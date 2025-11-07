from fastapi import FastAPI, Request
from utils.logger import get_logger

app = FastAPI(
    title="Hello World FastAPI Backend"
    )

logger = get_logger("backend")

@app.get("/")
async def hello(request: Request):
    user = request.headers.get("X-User", "Anonymous")
    logger.info(f"Request received from {user}")
    return {"message": f"Hello, {user}! Backend is working fine ✅"}
