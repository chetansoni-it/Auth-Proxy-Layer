from .base import BaseDB

class MySQLDB(BaseDB):
    async def verify_user(self, username: str, password: str) -> bool:
        raise NotImplementedError("MySQL integration not implemented yet.")

    async def close(self):
        pass
