from abc import ABC, abstractmethod
from collections.abc import Callable

from domain_classes.blueprint import Blueprint


class RepositoryInterface(ABC):
    @abstractmethod
    def __init__(self, get_blueprint: Callable[[str], Blueprint], **kwargs):
        """Init method to be implemented. Any client specific parameters will be passed via kwargs"""

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
    def find(self, filters: dict) -> list[dict] | None:
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
