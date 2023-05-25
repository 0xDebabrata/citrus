import os
import pickle
from typing import Any, List, Optional
from numpy import float32
from numpy._typing import NDArray
from citrusdb.db.index.hnswlib import HnswIndex
from citrusdb.utils.utils import ensure_valid_path


class Index:
    _db: HnswIndex
    _parameters: dict

    def __init__(
        self,
        name: str,
        max_elements: int = 1000,
        persist_directory: Optional[str] = None,
        M: int = 64,
        ef_construction: int = 200,
        allow_replace_deleted: bool = False,
    ):
        self._db = HnswIndex(id=name)

        self._parameters = {
            "index_name": name,
            "max_elements": max_elements,
            "persist_directory": persist_directory,
            "M": M,
            "ef_construction": ef_construction,
            "allow_replace_deleted": allow_replace_deleted,
        }

        if persist_directory:
            self._load_params()

            if ensure_valid_path(persist_directory, str(self._parameters["index_name"])):
                self._db.load_index(
                    os.path.join(
                        persist_directory, str(self._parameters["index_name"])
                    ),
                    allow_replace_deleted=bool(
                        self._parameters["allow_replace_deleted"]
                    ),
                )
            else:
                self._db.init_index(
                    max_elements=max_elements,
                    M=M,
                    ef_construction=ef_construction,
                    allow_replace_deleted=allow_replace_deleted,
                )
                self._save()
        else:
            self._db.init_index(
                max_elements=max_elements,
                M=M,
                ef_construction=ef_construction,
                allow_replace_deleted=allow_replace_deleted,
            )

    def add(
        self,
        ids,
        embeddings: Optional[NDArray[float32]],
        replace_deleted: bool,
    ):
        self._db.add_items(embeddings, ids, replace_deleted)
        if self._parameters["persist_directory"]:
            self._save()

    def _load_params(self):
        if ensure_valid_path(self._parameters["persist_directory"], ".citrus_params"):
            filename = os.path.join(
                self._parameters["persist_directory"], ".citrus_params"
            )
            with open(filename, "rb") as f:
                self._parameters = pickle.load(f)

    def delete_vectors(self, ids: List[int]):
        for id in ids:
            self._db.mark_deleted(id)
        if self._parameters["persist_directory"]:
            self._save()

    def _save(self):
        self._db.save_index(
            os.path.join(
                self._parameters["persist_directory"], self._parameters["index_name"]
            )
        )
        self._save_params()

    def _save_params(self):
        output_file = os.path.join(
            self._parameters["persist_directory"], ".citrus_params"
        )
        with open(output_file, "wb") as f:
            pickle.dump(self._parameters, f)

    def set_ef(self, ef: int):
        self._db.set_ef(ef)

    def query(
        self,
        documents: Optional[List[str]] = None,
        query_embeddings: Optional[NDArray[float32]] = None,
        k=1,
    ):
        if query_embeddings is None and documents is None:
            raise ValueError("Please provide either an embedding" + " or a document.")

        if documents is not None:
            from citrusdb.embedding.openai import get_embeddings

            embeddings = get_embeddings(documents)
            query_embeddings = embeddings

        return self._db.knn_query(query_embeddings, k)

    def get_status(self):
        self._db.get_status()

    def get_dimension(self):
        return self._db.get_dimension()

    def get_replace_deleted(self):
        return self._parameters["allow_replace_deleted"]

