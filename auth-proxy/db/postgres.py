import asyncpg
import os
from .base import BaseDB
from utils.logger import get_logger

logger = get_logger("postgres-db")

class PostgresDB(BaseDB):
    def __init__(self):
        self.pool = None
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT", 5432)
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")

    async def connect(self):
        """Initialize a connection pool."""
        try:
            self.pool = await asyncpg.create_pool(
                user=self.user,
                password=self.password,
                database=self.database,
                host=self.host,
                port=self.port,
                min_size=1,
                max_size=5,
            )
            logger.info(f"Connected to Postgres DB '{self.database}' at {self.host}")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise e

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            logger.info("Postgres connection pool closed.")

    async def verify_user(self, username: str, password: str) -> bool:
        """Verify username/password from 'users' table."""
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow(
                "SELECT * FROM users WHERE username=$1 AND password=$2",
                username, password
            )
            return result is not None
