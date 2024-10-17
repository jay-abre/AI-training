import httpx
import logging

async def send_message(page_access_token: str, recipient_id: str, message_text: str, message_type: str = "UPDATE"):
   
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