from fastapi import APIRouter, Request, HTTPException
from app.services.messaging import send_message
from app.db.database import log_collection
from app.models.models import UserMessage, BotMessage
import logging
import os

router = APIRouter()

VERIFY_TOKEN = "default_verify_token"
PAGE_ACCESS_TOKEN = "default_page_access_token"

@router.get("/")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    logging.info(f"Received mode: {mode}, token: {token}, challenge: {challenge}, expected token: {VERIFY_TOKEN}")

    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            logging.info("WEBHOOK_VERIFIED")
            return int(challenge)
        else:
            logging.error("Invalid token or mode")
            raise HTTPException(status_code=403, detail="Invalid token or mode")
    else:
        logging.error("Missing mode or token")
        raise HTTPException(status_code=400, detail="Missing mode or token")

@router.post("/")
async def receive_webhook(request: Request):
    try:
        webhook_data = await request.json()
        logging.info(f"Received webhook data: {webhook_data}")

        result = await log_collection.insert_one(webhook_data)
        logging.info(f"Inserted log with ID: {result.inserted_id}")

        for entry in webhook_data.get("entry", []):
            for messaging in entry.get("messaging", []):
                sender_id = messaging.get("sender", {}).get("id")
                message_text = messaging.get("message", {}).get("text")
                timestamp = messaging.get("timestamp")
                if sender_id and message_text:
                    user_message = UserMessage(
                        timestamp=timestamp,
                        text=message_text,
                        message_id=messaging.get("message", {}).get("mid"),
                        parse_data="",
                    )
                    await log_collection.insert_one(user_message.dict())
                    logging.info(f"Saved user message from {sender_id} with text: {message_text}")

                    bot_message = BotMessage(
                        timestamp=timestamp,
                        text=f"echo: {message_text}",
                        data="",
                    )
                    await log_collection.insert_one(bot_message.dict())
                    logging.info(f"Saved bot message with text: echo: {message_text}")

                    await send_message(
                        page_access_token=PAGE_ACCESS_TOKEN,
                        recipient_id=sender_id,
                        message_text=f"echo: {message_text}"
                    )

        return {"status": "success"}
    except Exception as e:
        logging.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=400, detail=str(e))