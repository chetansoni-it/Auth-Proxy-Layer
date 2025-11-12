from .base import BaseDB

class MongoDB(BaseDB):
    async def verify_user(self, username: str, password: str) -> bool:
        raise NotImplementedError("MongoDB integration not implemented yet.")

    async def close(self):
        pass
