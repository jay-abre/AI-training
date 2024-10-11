from fastapi import FastAPI, Request, HTTPException, Depends
from .database import log_collection
from bson import ObjectId
import logging
import os
from dotenv import load_dotenv
import httpx
import json

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

logging.basicConfig(level=logging.INFO)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "my_token")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

async def send_message(page_access_token: str, recipient_id: str, message_text: str, message_type: str = "UPDATE"):
    """
    Send message to specific user (by recipient ID) from specific page (by access token).

    Arguments:
        page_access_token: (string) Target page access token.
        recipient_id: (string) The ID of the user that the message is addressed to.
        message_text: (string) The content of the message.
        message_type: (string) The type of the target message.
    """
    r = httpx.post(
       "https://graph.facebook.com/v16.0/me/messages",
        params={"access_token": page_access_token},
        headers={"Content-Type": "application/json"},
        json={
            "recipient": {"id": recipient_id},
            "message": {"text": message_text},
            "messaging_type": message_type,
        },
    )
    r.raise_for_status()

@app.get("/messaging-webhook")
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

@app.post("/messaging-webhook")
async def receive_webhook(request: Request):
    try:
        webhook_data = await request.json()
        logging.info(f"Received webhook data: {webhook_data}")

        # Insert the raw webhook data into MongoDB
        result = await log_collection.insert_one(webhook_data)
        logging.info(f"Inserted log with ID: {result.inserted_id}")

        # Extract sender_id and message_text for sending a response
        for entry in webhook_data.get("entry", []):
            for messaging in entry.get("messaging", []):
                sender_id = messaging.get("sender", {}).get("id")
                message_text = messaging.get("message", {}).get("text")
                if sender_id and message_text:
                    await send_message(
                        page_access_token=PAGE_ACCESS_TOKEN,
                        recipient_id=sender_id,
                        message_text=f"echo: {message_text}"
                    )

        return {"status": "success"}
    except Exception as e:
        logging.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=400, detail=str(e))