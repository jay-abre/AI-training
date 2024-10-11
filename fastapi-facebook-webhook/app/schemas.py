from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    mid: str
    seq: int
    text: str

class Messaging(BaseModel):
    sender: dict
    recipient: dict
    timestamp: int
    message: Message

class Entry(BaseModel):
    id: str
    time: int
    messaging: List[Messaging]

class WebhookData(BaseModel):
    object: str
    entry: List[Entry]