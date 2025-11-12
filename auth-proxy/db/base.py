from abc import ABC, abstractmethod

class BaseDB(ABC):
    """Abstract base class for DB authentication backends."""

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    async def verify_user(self, username: str, password: str) -> bool:
        """Return True if username/password is valid."""
        pass
