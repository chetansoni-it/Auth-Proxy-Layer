from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from utils.logger import get_logger
from db import get_database
import os

load_dotenv()

app = FastAPI(
    title="Auth Proxy Service"
    )

logger = get_logger("auth-proxy")

# Load DB dynamically
db = get_database()

@app.on_event("startup")
async def startup_event():
    await db.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await db.disconnect()


# Middleware for authentication, can be replaced with JWT/OAuth later
# only /health is excluded from authentication
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """
    Acts as an authentication layer for incoming requests.
    In future, you can swap this for JWT or OAuth verification.
    """

    # Skip authentication for specific endpoints
    if request.url.path in ["/health"]:
        return await call_next(request)

    # Example: Basic Auth (Authorization: Basic base64encoded(username:password))
    # For now, we’ll accept simple headers: X-User and X-Password
    user = request.headers.get("X-User")
    password = request.headers.get("X-Password")

    # Validate from DB
    if user and password and await db.verify_user(user, password):
        # Auth successful — log and add header for backend
        logger.info(f"✅ Auth success: {user}")
        response = await call_next(request)
        response.headers["X-User"] = user
        return response

    logger.warning(f"❌ Unauthorized access attempt by {user or 'unknown'}")
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": "Unauthorized - Invalid credentials"},
    )

@app.get("/health")
async def health_check():
    return {"status": "Auth Proxy running fine ✅"}

@app.get("/test-auth")
async def test_auth(request: Request):
    user = request.headers.get("X-User", "Anonymous")
    return {"message": f"Hello {user}, Auth Proxy is up and running!"}


# ### Old hardcoded version for reference
# FAKE_USER_ID = os.getenv("FAKE_USER_ID", "admin")
# FAKE_USER_PASSWORD = os.getenv("FAKE_USER_PASSWORD", "admin123")

# # Middleware for authentication, can be replaced with JWT/OAuth later
# # only /health is excluded from authentication

# @app.middleware("http")
# async def auth_middleware(request: Request, call_next):
#     """
#     Acts as an authentication layer for incoming requests.
#     In future, you can swap this for JWT or OAuth verification.
#     """

#     # Skip authentication for specific endpoints
#     if request.url.path in ["/health"]:
#         return await call_next(request)

#     # Example: Basic Auth (Authorization: Basic base64encoded(username:password))
#     # For now, we’ll accept simple headers: X-User and X-Password
#     user = request.headers.get("X-User")
#     password = request.headers.get("X-Password")

#     if user == FAKE_USER_ID and password == FAKE_USER_PASSWORD:
#         # Auth successful — log and add header for backend
#         logger.info(f"User '{user}' authenticated successfully.")
#         response = await call_next(request)
#         response.headers["X-User"] = user
#         return response
#     else:
#         logger.warning("Unauthorized access attempt.")
#         return JSONResponse(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             content={"error": "Unauthorized - Invalid credentials"},
#         )
