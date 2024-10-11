from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://user:password@localhost:27017")

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.webhook_db
log_collection = database.get_collection("logs")