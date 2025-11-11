# NGINX Reverse Proxy with Authentication Layer

This configuration sets up an **NGINX reverse proxy** that protects access to your backend service using an **authentication proxy**.  
It uses the `auth_request` directive to validate requests before forwarding them to the backend.

---

## 📁 File Overview

**File:** `nginx.conf`  
**Purpose:** To route traffic through NGINX, authenticate users via a secondary service, and forward authorized requests to a backend application.

---

## ⚙️ Configuration Breakdown

### 1. Worker Configuration
```nginx
worker_processes auto;
events { worker_connections 1024; }
```
- **`worker_processes auto`** — Automatically adjusts to the number of available CPU cores.
- **`worker_connections 1024`** — Each worker process can handle up to 1024 simultaneous connections.

---

### 2. Upstream Definitions
```nginx
upstream backend_service {
    server backend:8000;
}

upstream auth_proxy {
    server auth-proxy:8001;
}
```
Defines two backend services:
- **`backend_service`** → The main application (running on port 8000).
- **`auth_proxy`** → Authentication service (running on port 8001).

These services communicate within the same Docker network.

---

### 3. Main Server Block
```nginx
server {
    listen 80;
```
- Listens for incoming HTTP requests on **port 80**.

---

### 4. Main Route (`/`)
```nginx
location / {
    auth_request /auth;
    proxy_pass http://backend_service;
    proxy_set_header X-User $remote_user;
}
```
- `auth_request /auth` — Sends a subrequest to `/auth` before proxying to the backend.  
  If `/auth` returns 2xx → allow the request; otherwise → reject.
- `proxy_pass` — Forwards authorized traffic to the backend.
- `proxy_set_header` — Passes the authenticated user to downstream services.

---

### 5. Authentication Subrequest (`/auth`)
```nginx
location = /auth {
    internal;
    proxy_pass http://auth_proxy/test-auth;
    proxy_pass_request_body off;
    proxy_set_header Content-Length "";
    proxy_set_header X-User $http_x_user;
    proxy_set_header X-Password $http_x_password;
}
```
- `internal` — Makes this route inaccessible externally.
- Proxies the auth check to the `auth-proxy` service’s `/test-auth` endpoint.
- Disables sending request bodies (auth checks usually only need headers).
- Forwards user credentials via headers for validation.

---

### 6. Health Check (`/auth-proxy-health`)
```nginx
location /auth-proxy-health {
    proxy_pass http://auth_proxy/health;
}
```
- Provides a simple health endpoint to verify that the Auth-Proxy service is reachable.

---

## 🧠 Summary

| Section | Purpose |
|----------|----------|
| **upstream backend_service** | Routes traffic to the main backend service |
| **upstream auth_proxy** | Handles authentication requests |
| **auth_request /auth** | Performs access validation before passing traffic |
| **/auth block** | Internal route for authentication subrequests |
| **/auth-proxy-health** | Used for health or readiness probes |

---

## 🚀 How It Works (Flow)

1. A client sends a request to NGINX (`/`).
2. NGINX first calls `/auth` internally.
3. The `/auth` subrequest contacts the `auth-proxy` service for validation.
4. If successful (HTTP 2xx), the request is forwarded to the backend.
5. Otherwise, NGINX blocks the request with an error (401 or 403).

---

## 🔒 Optional Enhancements

- Add HTTPS and redirect HTTP → HTTPS for production.
- Cache authentication results for better performance.
- Include rate limiting or IP whitelisting.

---

## 🧩 Example Docker Setup

Example `docker-compose.yml` fragment:
```yaml
services:
  nginx:
    image: nginx:latest
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "80:80"
    depends_on:
      - backend
      - auth-proxy

  backend:
    build: ./backend

  auth-proxy:
    build: ./auth-proxy
```

---

## ✅ Health Verification

Once running, test routes:

| Endpoint | Description | Expected |
|-----------|-------------|-----------|
| `/` | Main backend route (auth protected) | 200 OK after valid auth |
| `/auth` | Internal auth endpoint | Inaccessible externally |
| `/auth-proxy-health` | Health probe route | 200 OK if Auth-Proxy is healthy |

---

## 🧾 License

This configuration is provided for educational and internal use under the MIT License.
