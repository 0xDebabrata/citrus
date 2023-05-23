from citrusdb.api.index import Index
from citrusdb.db.sqlite.db import DB

from typing import Dict, List, Optional
from numpy import float32
from numpy._typing import NDArray


class LocalAPI:
    _db: Dict[str, Index] 
    _sqlClient: DB
    persist_directory: Optional[str]

    def __init__(self, persist_directory: Optional[str] = None):
        self._db = {}
        self.persist_directory = persist_directory

        if persist_directory is not None:
            self._sqlClient = DB(persist_directory)

    def create_index(
        self,
        name: str,
        max_elements: int = 1000,
        M: int = 64,
        ef_construction: int = 200,
        allow_replace_deleted: bool = False,
    ):
        if self.persist_directory is not None and not(self._sqlClient.get_index_details(name)):
            self._sqlClient.create_index(
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
        metadatas: Optional[Dict] = None
    ):
        """
        Insert embeddings/text documents
        index: Name of index
        ids: Unique ID for each element
        documents: List of strings to index
        embeddings: List of embeddings to index
        """

        if embeddings is None and documents is None:
            raise ValueError("Please provide either embeddings or documents.")

        if self.persist_directory is not None:
            index_details = self._sqlClient.get_index_details(index)
            if index_details is None:
                raise ValueError(f"Index with name '{index}' does not exist.")

            if documents is not None:
                from citrusdb.embedding.openai import get_embeddings

                embeddings = get_embeddings(documents)

            if embeddings is not None:
                embedding_dim = len(embeddings[0])
                index_id = index_details[0]
                index_dim = index_details[2]
                replace_deleted = index_details[7]
                print(index_id, index_dim, replace_deleted)

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
                        None if metadatas is None else metadatas[i]
                    )
                    data.append(row)

                if self.persist_directory is not None:
                    self._sqlClient.insert_to_index(data)
        else:
            flag = 1
            for key in self._db.keys():
                if key == index:
                    flag = 0
                    break
            if flag:
                raise ValueError(f"Index with name '{index}' does not exist.")

            if documents is not None:
                from citrusdb.embedding.openai import get_embeddings

                embeddings = get_embeddings(documents)

            if embeddings is not None:
                embedding_dim = len(embeddings[0])
                index_dim = self._db[index].get_dimension()
                replace_deleted = self._db[index].get_replace_deleted()

                self._db[index].add(
                    ids=ids,
                    embeddings=embeddings,
                    replace_deleted=replace_deleted
                )

    def set_ef(self, index: str, ef: int):
        if self.persist_directory is not None:
            self._sqlClient.update_ef(index, ef)

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
