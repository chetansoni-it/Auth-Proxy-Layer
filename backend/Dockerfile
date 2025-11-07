FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir fastapi[standard]==0.121.0 python-dotenv

EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--port", "8000", "--host", "0.0.0.0"]
