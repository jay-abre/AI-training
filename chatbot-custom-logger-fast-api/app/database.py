from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Read the MongoDB URL from the environment variable
mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/chatbot_db')

# Create a MongoDB client
client = MongoClient(mongo_url)

# Access the database
db = client["chatbot_db"]

def get_db():
    return db