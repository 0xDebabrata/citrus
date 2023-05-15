import os
import pickle
from citrusdb.api.index import Index

from typing import Dict, List, Optional
from numpy import float32
from numpy._typing import NDArray


class LocalAPI:
    _db: Dict[str, Index] 
    _parameters: dict

    def __init__(self):
        self._db = {}

    def create_index(
        self,
        name,
        max_elements: int = 1000,
        persist_directory: Optional[str] = None,
        M: int = 64,
        ef_construction: int = 200,
        allow_replace_deleted: bool = False,
    ):
        self._db[name] = Index(
            name=name,
            max_elements=max_elements,
            persist_directory=persist_directory,
            M=M,
            ef_construction=ef_construction,
            allow_replace_deleted=allow_replace_deleted
        )

    def add(
        self,
        index: str,
        ids,
        documents: Optional[List[str]] = None,
        embeddings: Optional[NDArray[float32]] = None,
    ):
        flag = 1
        for key in self._db.keys():
            if key == index:
                flag = 0
                self._db[key].add(
                    ids=ids,
                    documents=documents,
                    embeddings=embeddings
                )

        if flag:
            raise ValueError(f"Could not find index: {index}")

    def _load_params(self):
        if os.path.exists(
            os.path.join(self._parameters["persist_directory"], ".citrus_params")
        ):
            filename = os.path.join(
                self._parameters["persist_directory"], ".citrus_params"
            )
            with open(filename, "rb") as f:
                self._parameters = pickle.load(f)

    def set_ef(self, index: str, ef: int):
        flag = 1
        for key in self._db.keys():
            if key == index:
                flag = 0
                self._db[key].set_ef(ef)

        if flag:
            raise ValueError(f"Could not find index: {index}")

    def query(
        self,
        index: str,
        documents: Optional[List[str]] = None,
        query_embeddings: Optional[NDArray[float32]] = None,
        k=1,
    ):
        flag = 1
        for key in self._db.keys():
            if key == index:
                flag = 0
                return self._db[key].query(
                    documents=documents,
                    query_embeddings=query_embeddings,
                    k=k
                )

        if flag:
            raise ValueError(f"Could not find index: {index}")


    def get_status(self, index: str):
        flag = 1
        for key in self._db.keys():
            if key == index:
                flag = 0
                self._db[key].get_status()

        if flag:
            raise ValueError(f"Could not find index: {index}")
