from fastapi import FastAPI
from app.routes.user_routes import user_router
from app.routes.bot_routes import bot_router

app = FastAPI()

app.include_router(user_router)
app.include_router(bot_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Chatbot Logger API!"}
