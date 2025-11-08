### 📘 **Traefik README**

**File:** `./traefik/README.md`

# Traefik Reverse Proxy

Traefik is used as the reverse proxy and router that connects the Auth Proxy and Backend securely.

---

## ⚙️ Files
```bash
traefik/
│-- traefik.yml
│-- dynamic_conf.yml
```

---

## 📜 Configuration Details

### `traefik.yml`
Defines entry points and provider:
```yaml
api:
  insecure: true
  dashboard: true

entryPoints:
  web:
    address: ":80"

providers:
  file:
    filename: /etc/traefik/dynamic_conf.yml
    watch: true
```

### `dynamic_conf.yml`
Defines routing and middleware:
```yaml
http:
  routers:
    backend-router:
      rule: "PathPrefix(`/`)"
      service: backend-service
      entryPoints:
        - web
      middlewares:
        - auth-mw

  services:
    backend-service:
      loadBalancer:
        servers:
          - url: "http://backend:8000"

  middlewares:
    auth-mw:
      forwardAuth:
        address: "http://auth-proxy:8001/test-auth"
        trustForwardHeader: true
```
---

## 🧭 Dashboard

Access the Traefik dashboard:
👉 http://localhost:8080/dashboard/

### 🧠 Notes

- Traefik listens on port 80 for incoming requests.
- All requests are routed to the backend after passing through the auth-proxy.
- Configuration auto-reloads on file changes.

### 🔧 Useful Commands
```bash
docker compose logs traefik
docker compose restart traefik
```