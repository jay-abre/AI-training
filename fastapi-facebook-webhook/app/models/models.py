# app/models/models.py
from pydantic import BaseModel
from typing import Optional

class UserMessage(BaseModel):
    event: str = "user"
    timestamp: int
    text: str
    message_id: str
    parse_data: str
    data: Optional[None] = None

class BotMessage(BaseModel):
    event: str = "bot"
    timestamp: int
    text: str
    data: str
    message_id: Optional[None] = None
    parse_data: Optional[None] = None