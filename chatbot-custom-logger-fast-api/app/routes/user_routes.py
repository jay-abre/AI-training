from fastapi import APIRouter, HTTPException, status, Depends
from app.models import UserEvent
from app.database import get_db
from bson import ObjectId
from pymongo.errors import PyMongoError
from app.custom_logging import logger

user_router = APIRouter()

@user_router.post("/log/user", status_code=status.HTTP_201_CREATED)
async def log_user_event(event: UserEvent, db = Depends(get_db)):
    collection = db["user_logs"]
    event_dict = event.dict()
    try:
        result = collection.insert_one(event_dict)
        event_dict["_id"] = str(result.inserted_id)  
        logger.info(f"User event logged: {event_dict}")
        return {"message": "User event logged successfully", "event": event_dict}
    except PyMongoError as e:
        logger.error(f"Error logging user event: {e}")
        raise HTTPException(status_code=500, detail=str(e))