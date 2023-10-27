from abc import ABC, abstractmethod
from typing import Optional


class RepositoryInterface(ABC):
    @abstractmethod
    def add(self, uid: str, document: dict) -> bool:
        """Get method to be implemented"""

    @abstractmethod
    def update(self, uid: str, document: dict) -> bool:
        """Update method to be implemented"""

    @abstractmethod
    def get(self, uid: str) -> dict:
        """Get method to be implemented"""

    @abstractmethod
    def delete(self, uid: str) -> bool:
        """Delete method to be implemented"""

    @abstractmethod
    def find(self, filters: dict) -> Optional[list[dict]]:
        """Find method to be implemented"""

    @abstractmethod
    def find_one(self, filters: dict) -> dict:
        """Find one method to be implemented"""

    @abstractmethod
    def update_blob(self, uid: str, blob: bytearray):
        """Update blob method to be implemented"""

    @abstractmethod
    def delete_blob(self, uid: str):
        """Delete blob method to be implemented"""

    @abstractmethod
    def get_blob(self, uid: str) -> bytearray:
        """Get blob method to be implemented"""
