from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple, Optional

from citrusdb.utils.types import IDs


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
        ids: IDs
    ) -> List[int]:
        pass

    @abstractmethod
    def filter_vectors(self, index_name: str, filters: List[Dict]) -> List:
        pass

    @abstractmethod
    def get_indices(self) -> List[Any]:
        pass

    @abstractmethod
    def get_index_details(
        self,
        name: str
    ) -> Optional[Tuple[int, str, int, int, int, int, int, bool]]:
        pass

    @abstractmethod
    def get_vector_ids_of_results(
        self,
        name: str,
        results: List[List[int]],
        include: Dict
    ) -> List[List[Dict]]:
        pass

    @abstractmethod
    def insert_to_index(
        self,
        data
    ) -> List[int]:
        pass

    @abstractmethod
    def update_ef(
        self,
        name: str,
        ef: int
    ):
        pass

