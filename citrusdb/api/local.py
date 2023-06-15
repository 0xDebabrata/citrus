import os
import json
from typing import Any, Dict, List, Optional
from numpy import float32
from numpy._typing import NDArray
import shutil

from citrusdb.api.index import Index
from citrusdb.db import BaseDB
from citrusdb.db.postgres.db import PostgresDB
from citrusdb.db.sqlite.db import SQLiteDB


class LocalAPI:
    _db: Dict[str, Index] 
    _SQLClient: BaseDB
    persist_directory: Optional[str]
    _TEMP_DIRECTORY = "citrus_temp"

    def __init__(
        self,
        persist_directory: Optional[str] = None,
        database_type: Optional[str] = "sqlite",
        **kwargs: Optional[Dict[str, Any]]
    ):
        self._db = {}
        self.persist_directory = persist_directory

        if not(persist_directory) and os.path.isdir(self._TEMP_DIRECTORY):
            # Cleanup previous sqlite data
            shutil.rmtree(self._TEMP_DIRECTORY)

        if persist_directory and database_type == "pg":
            self._SQLClient = PostgresDB(**kwargs)
        else:
            self._SQLClient = SQLiteDB(persist_directory if persist_directory else self._TEMP_DIRECTORY)

    def create_index(
        self,
        name: str,
        max_elements: int = 1000,
        M: int = 64,
        ef_construction: int = 200,
        allow_replace_deleted: bool = False,
    ):
        if not(self._SQLClient.get_index_details(name)):
            self._SQLClient.create_index(
                name,
                max_elements,
                M,
                ef_construction,
                allow_replace_deleted
            )

        self._db[name] = Index(
            name=name,
            max_elements=max_elements,
            persist_directory=self.persist_directory,
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
        metadatas: Optional[List[Dict]] = None
    ):
        """
        Insert embeddings/text documents
        index: Name of index
        ids: Unique ID for each element
        documents: List of strings to index
        embeddings: List of embeddings to index
        metadatas: Additional metadata for each vector
        """

        if embeddings is None and documents is None:
            raise ValueError("Please provide either embeddings or documents.")

        index_details = self._SQLClient.get_index_details(index)
        if index_details is None:
            raise ValueError(f"Index with name '{index}' does not exist.")

        if (documents is not None) and (embeddings is None):
            from citrusdb.embedding.openai import get_embeddings

            embeddings = get_embeddings(documents)

        if embeddings is not None:
            embedding_dim = len(embeddings[0])
            index_id = index_details[0]
            index_dim = index_details[2]
            replace_deleted = True if index_details[7] else False

            # Check whether the dimensions are equal
            if embedding_dim != index_dim:
                raise ValueError(
                        f"Embedding dimenstion ({embedding_dim}) and index "
                        + f"dimension ({index_dim}) do not match."
                        )

            # Ensure no of ids = no of embeddings
            if len(ids) != len(embeddings):
                raise ValueError(f"Number of embeddings" + " and ids are different.")

            data = []
            for i in range(len(ids)):
                row = (
                    ids[i],
                    index_id,
                    None if documents is None else documents[i],
                    embeddings[i],
                    None if metadatas is None else json.dumps(metadatas[i])
                )
                data.append(row + row)

            # Insert data into sqlite
            self._SQLClient.insert_to_index(data)

            # Index vectors
            self._db[index].add(
                ids=ids,
                embeddings=embeddings,
                replace_deleted=replace_deleted
            )

    def delete_vectors(
        self,
        index: str,
        ids: List[int],
    ):
        index_details = self._SQLClient.get_index_details(index)
        if index_details is None:
            raise ValueError(f"Could not find index: {index}")

        index_id = index_details[0]
        self._SQLClient.delete_vectors_from_index(
            index_id=index_id,
            ids=ids
        )

        self._db[index].delete_vectors(ids)

    def reload_indices(self):
        """
        Load all indices from disk to memory
        """

        indices = self._SQLClient.get_indices()
        for index in indices:
            index_name = index[1]
            # Load index
            self.create_index(
                name=index_name,
                max_elements=index[3],
                M=index[4],
                ef_construction=index[6],
                allow_replace_deleted=index[7]
            )
            # Set ef value
            self._db[index_name].set_ef(index[5])

    def set_ef(self, index: str, ef: int):
        index_details = self._SQLClient.get_index_details(index)
        if index_details is None:
            raise ValueError(f"Could not find index: {index}")

        self._SQLClient.update_ef(index, ef)
        self._db[index].set_ef(ef)

    def query(
        self,
        index: str,
        documents: Optional[List[str]] = None,
        query_embeddings: Optional[NDArray[float32]] = None,
        k=1,
        filters: Optional[List[Dict]] = None
    ):
        allowed_ids = []
        if filters is not None:
            allowed_ids = self._SQLClient.filter_vectors(index, filters)

        filter_function = lambda label: str(label) in allowed_ids

        flag = 1
        for key in self._db.keys():
            if key == index:
                flag = 0
                return self._db[key].query(
                    documents=documents,
                    query_embeddings=query_embeddings,
                    k=k,
                    filter_function=None if filters is None else filter_function
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
