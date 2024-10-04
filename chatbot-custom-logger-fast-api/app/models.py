from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserEvent(BaseModel):
    sender_id: str = Field(..., min_length=1)
    event: str = Field(..., min_length=1)
    timestamp: datetime
    text: str = Field(..., min_length=1)
    message_id: str = Field(..., min_length=1)
    parse_data: Optional[dict] = None
    data: Optional[dict] = None

class BotEvent(BaseModel):
    sender_id: str = Field(..., min_length=1)
    event: str = Field(..., min_length=1)
    timestamp: datetime
    text: str = Field(..., min_length=1)
    data: Optional[dict] = None
    message_id: Optional[str] = None
    parse_data: Optional[dict] = None