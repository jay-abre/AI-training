# models.py
from pydantic import BaseModel, Field
from typing import Optional

class Log(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    sender_id: str
    message: str
    timestamp: str