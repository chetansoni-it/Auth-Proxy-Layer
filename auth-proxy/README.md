### 📙 **Auth Proxy README**

**File:** `./auth-proxy/README.md`

# Auth Proxy (FastAPI)

The Auth Proxy acts as a gatekeeper in front of all backend APIs.
It validates requests before forwarding to the backend.

---

## ⚙️ Features
- Header-based authentication (`X-User`, `X-Password`)
- Configurable credentials from `.env`
- `/health` and `/test-auth` endpoints for monitoring
- Structured JSON logging

---

## 🧩 Folder Structure
```bash
auth-proxy/
│-- main.py
│-- utils/logger.py
│-- pyproject.toml
│-- Dockerfile
│-- .env
```

---

## ⚙️ Environment Variables (`.env`)
```bash
AUTH_PROXY_PORT=8001
FAKE_USER_ID=admin
FAKE_USER_PASSWORD=admin123
```
---

## 🏃 Run Locally
1. Using FastAPI
```bash
fastapi run main.py
```

2. Test Auth Logic
```bash
curl http://localhost:8001/health
# → {"status":"Auth Proxy running fine ✅"}

curl -H "X-User: admin" -H "X-Password: admin123" http://localhost:8001/test-auth
# → {"message":"Hello admin, Auth Proxy is up and running!"}
```
---

### 🐳 Run in Docker
```bash
docker build -t auth-proxy:latest .
docker run -p 8001:8001 auth-proxy:latest
```
---

## 🔒 How It Works

- Traefik forwards incoming requests to /test-auth.
- If the Auth Proxy validates headers, it returns 200 OK and the request proceeds.
- If invalid, it returns 401 Unauthorized.
---


### 🧠 Notes

- Replace fake header check with JWT, OAuth2, or Database Auth for production.
- The proxy can easily scale independently from the backend.

---
### 🔧 Useful Commands
```bash
docker compose logs auth-proxy
docker compose restart auth-proxy
```
