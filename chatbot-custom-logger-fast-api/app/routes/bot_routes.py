from fastapi import APIRouter, HTTPException, status, Depends
from app.models import BotEvent
from app.database import get_db
from bson import ObjectId
from pymongo.errors import PyMongoError
from app.logging import logger

bot_router = APIRouter()

@bot_router.post("/log/bot", status_code=status.HTTP_201_CREATED)
async def log_bot_event(event: BotEvent, db = Depends(get_db)):
    collection = db["bot_logs"]
    event_dict = event.dict()
    try:
        result = collection.insert_one(event_dict)
        event_dict["_id"] = str(result.inserted_id)  
        logger.info(f"Bot event logged: {event_dict}")
        return {"message": "Bot event logged successfully", "event": event_dict}
    except PyMongoError as e:
        logger.error(f"Error logging bot event: {e}")
        raise HTTPException(status_code=500, detail=str(e))