### 📗 **Backend README**

**File:** `./backend/README.md`

# Backend Service (FastAPI)

This is the core FastAPI microservice that handles business logic.

## ⚙️ Features
- Simple Hello World API
- Structured Logging (JSON format)
- Ready for future modular endpoints

---

## 🧩 Folder Structure
```bash
backend/
│-- main.py
│-- utils/logger.py
│-- pyproject.toml
│-- Dockerfile
```

---

## 🏃 Run Locally

### 1. Using FastAPI
```bash
fastapi run main.py
```

### 2. Test Endpoint
```bash
curl http://localhost:8000/
# → {"message":"Hello, Anonymous! Backend is working fine ✅"}
```

---
### 🐳 Run in Docker
```bash
docker build -t backend:latest .
docker run -p 8000:8000 backend:latest
```

### 🧠 Notes

- All logs are structured JSON via utils/logger.py.
- The backend trusts authentication headers forwarded by the Auth Proxy.
- For production, avoid running directly — always use via Traefik or Auth Proxy.
---

### 🔧 Useful Commands
```bash
docker compose logs backend
docker compose restart backend
```
