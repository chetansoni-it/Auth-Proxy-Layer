FROM python:3.11-slim

WORKDIR /app

# Install curl and uv
RUN apt-get update && apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    rm -rf /var/lib/apt/lists/*

# Make sure uv is in PATH
ENV PATH="/root/.cargo/bin:/root/.local/bin:$PATH"

COPY . .

# Sync dependencies (this installs virtualenv + dependencies)
RUN uv sync

EXPOSE 8000

# Use uv’s virtual environment automatically
CMD ["uv", "run", "fastapi", "run", "main.py", "--port", "8000", "--host", "0.0.0.0"]