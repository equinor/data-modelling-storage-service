from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class RepositoryInterface(ABC):
    @abstractmethod
    def add(self, uid: str, document: Dict) -> bool:
        """Get method to be implemented"""

    @abstractmethod
    def update(self, uid: str, document: Dict) -> bool:
        """Update method to be implemented"""

    @abstractmethod
    def get(self, uid: str) -> Dict:
        """Get method to be implemented"""

    @abstractmethod
    def delete(self, uid: str) -> bool:
        """Delete method to be implemented"""

    @abstractmethod
    def find(self, filters: Dict) -> Optional[List[Dict]]:
        """Find method to be implemented"""

    @abstractmethod
    def find_one(self, filters: Dict) -> Dict:
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
