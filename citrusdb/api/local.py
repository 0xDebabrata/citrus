from typing import List
import numpy as np
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
    
    def add(self, embedding: List[List[float]], ids):
        embedding_dim = len(embedding[0])
        index_dim = self._db.get_dimension()

        # Check whether the dimensions are equal
        if (embedding_dim != index_dim):
            raise ValueError(
                    f"Embedding dimenstion ({embedding_dim}) and index " +
                    f"dimension ({index_dim}) do not match.")

        # Ensure no of ids = no of embeddings
        if (len(ids) != len(embedding)):
            raise ValueError(f"Number of embeddings and ids are different.")

        self._db.add_items(embedding, ids)

    def query(self, query_embedding, k = 1):
        labels, distances = self._db.knn_query(query_embedding, k)
        print(labels)
        print(distances)

    def get_status(self):
        self._db.get_status()


