from typing import List, Optional
from citrusdb.db.index.hnswlib import HnswIndex

class LocalAPI:
    _db: HnswIndex

    def __init__(self):
        self._db = HnswIndex(
                id="test")

    def create_index(
            self, 
            max_elements = 1000, 
            M = 16, 
            ef_construction = 200, 
            allow_replace_deleted = False):

        self._db.init_index(
                max_elements=max_elements,
                M=M,
                ef_construction=ef_construction,
                allow_replace_deleted=allow_replace_deleted)
    
    def add(
            self, 
            ids,
            documents: Optional[List[str]] = None,
            embedding: Optional[List[List[float]]] = None):

        if embedding == None and documents == None:
            raise ValueError("Please provide either embeddings or documents.")

        if documents:
            from citrusdb.embedding.openai import get_embeddings
            embedding = get_embeddings(documents)

        if embedding:
            embedding_dim = len(embedding[0])
            index_dim = self._db.get_dimension()

            # Check whether the dimensions are equal
            if (embedding_dim != index_dim):
                raise ValueError(
                        f"Embedding dimenstion ({embedding_dim}) and index " +
                        f"dimension ({index_dim}) do not match.")

            # Ensure no of ids = no of embeddings
            if (len(ids) != len(embedding)):
                raise ValueError(f"Number of embeddings" +
                                " and ids are different.")

            self._db.add_items(embedding, ids)

    def query(
            self,
            document: Optional[str] = None,
            query_embedding: Optional[List[float]] = None,
            k = 1):

        if query_embedding== None and document == None:
            raise ValueError("Please provide either an embedding" +
                             " or a document.")

        if document:
            from citrusdb.embedding.openai import get_embeddings
            embedding = get_embeddings([document])
            query_embedding = embedding[0]

        return self._db.knn_query(query_embedding, k)

    def get_status(self):
        self._db.get_status()


