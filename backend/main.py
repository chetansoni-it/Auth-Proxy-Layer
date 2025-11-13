import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from utils.logger import get_logger

load_dotenv()

app = FastAPI(
    title="Hello World FastAPI Backend",
    version=os.getenv("BACKEND_VERSION")
    )

logger = get_logger("backend")

@app.get("/")
async def hello(request: Request):
    user = request.headers.get("X-User", "Anonymous")
    logger.info(f"Request received from {user}")
    return {"message": f"Hello, {user}! Backend is working fine ✅, running version " + os.getenv("BACKEND_VERSION")}

@app.get("/api/user")
async def get_user_info(request: Request):
    user = request.headers.get("X-User", "Anonymous")
    logger.info(f"User info requested by {user}")
    return {"user": user}