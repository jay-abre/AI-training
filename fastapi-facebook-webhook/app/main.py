from fastapi import FastAPI
from app.api.endpoints import webhook
from dotenv import load_dotenv
import logging
import os

load_dotenv()

app = FastAPI()

logging.basicConfig(level=logging.INFO)


webhook.VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
webhook.PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

app.include_router(webhook.router, prefix="/messaging-webhook")

