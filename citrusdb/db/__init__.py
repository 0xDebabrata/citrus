from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional


class BaseDB(ABC):
    @abstractmethod
    def create_index(
        self,
        name: str,
        max_elements: int,
        M: int,
        ef_construction: int,
        allow_replace_deleted: bool,
        dimensions: Optional[int] = 1536,
    ):
        pass

    @abstractmethod
    def delete_vectors_from_index(
        self,
        index_id: int,
        ids: List[int]
    ):
        pass

    @abstractmethod
    def filter_vectors(self, index_name: str, filters: List[Dict]) -> List:
        pass

    @abstractmethod
    def get_indices(self):
        pass

    @abstractmethod
    def get_index_details(
        self,
        name: str
    ) -> Optional[Tuple[int, str, int, int, int, int, int, bool]]:
        pass

    @abstractmethod
    def insert_to_index(
        self,
        data
    ):
        pass

    @abstractmethod
    def update_ef(
        self,
        name: str,
        ef: int
    ):
        pass

