import os
import pickle
from typing import Any, List, Optional
from numpy import float32
from numpy._typing import NDArray
from citrusdb.db.index.hnswlib import HnswIndex


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
            if os.path.exists(
                os.path.join(persist_directory, str(self._parameters["index_name"]))
            ):
                self._db.load_index(
                    os.path.join(
                        persist_directory, str(self._parameters["index_name"])
                    ),
                    allow_replace_deleted=bool(
                        self._parameters["allow_replace_deleted"]
                    ),
                )
            else:
                if not (os.path.isdir(persist_directory)):
                    os.makedirs(persist_directory)

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
        documents: Optional[List[str]] = None,
        embeddings: Optional[NDArray[float32]] = None,
    ):
        if embeddings is None and documents is None:
            raise ValueError("Please provide either embeddings or documents.")

        if documents is not None:
            from citrusdb.embedding.openai import get_embeddings

            embeddings = get_embeddings(documents)

        if embeddings is not None:
            embedding_dim = len(embeddings[0])
            index_dim = self._db.get_dimension()

            # Check whether the dimensions are equal
            if embedding_dim != index_dim:
                raise ValueError(
                    f"Embedding dimenstion ({embedding_dim}) and index "
                    + f"dimension ({index_dim}) do not match."
                )

            # Ensure no of ids = no of embeddings
            if len(ids) != len(embeddings):
                raise ValueError(f"Number of embeddings" + " and ids are different.")

            self._db.add_items(embeddings, ids)
            if self._parameters["persist_directory"]:
                self._save()

    def _load_params(self):
        if os.path.exists(
            os.path.join(self._parameters["persist_directory"], ".citrus_params")
        ):
            filename = os.path.join(
                self._parameters["persist_directory"], ".citrus_params"
            )
            with open(filename, "rb") as f:
                self._parameters = pickle.load(f)

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

