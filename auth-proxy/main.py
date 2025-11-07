from fastapi import FastAPI, Request, Response, status, Depends
from fastapi.responses import JSONResponse
from utils.logger import get_logger
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Auth Proxy Service"
    )

logger = get_logger("auth-proxy")

FAKE_USER_ID = os.getenv("FAKE_USER_ID", "admin")
FAKE_USER_PASSWORD = os.getenv("FAKE_USER_PASSWORD", "admin123")

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """
    Acts as an authentication layer for incoming requests.
    In future, you can swap this for JWT or OAuth verification.
    """
    auth_header = request.headers.get("Authorization")

    # Example: Basic Auth (Authorization: Basic base64encoded(username:password))
    # For now, we’ll accept simple headers: X-User and X-Password
    user = request.headers.get("X-User")
    password = request.headers.get("X-Password")

    if user == FAKE_USER_ID and password == FAKE_USER_PASSWORD:
        # Auth successful — log and add header for backend
        logger.info(f"User '{user}' authenticated successfully.")
        response = await call_next(request)
        response.headers["X-User"] = user
        return response
    else:
        logger.warning("Unauthorized access attempt.")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Unauthorized - Invalid credentials"},
        )

@app.get("/health")
async def health_check():
    """Simple health check for proxy."""
    return {"status": "Auth Proxy running fine ✅"}

@app.get("/test-auth")
async def test_auth(request: Request):
    """For testing direct access."""
    user = request.headers.get("X-User", "Anonymous")
    return {"message": f"Hello {user}, Auth Proxy is up and running!"}
