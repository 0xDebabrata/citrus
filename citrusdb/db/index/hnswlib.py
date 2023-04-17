import hnswlib

class HnswIndex:
    _id: str
    _index: hnswlib.Index

    def __init__(self, id, space = "cosine", dim = 1536):
        self._id = id
        self._index = hnswlib.Index(
                space = space,
                dim = dim)

    def init_index(
            self,
            max_elements = 1000,
            M = 16,
            ef_construction = 200,
            allow_replace_deleted = False):
        self._index.init_index(
                max_elements,
                M,
                ef_construction,
                allow_replace_deleted)

    def add_items(
            self,
            data,
            ids,
            replace_deleted = False):
        max_elements = self._index.max_elements
        curr_elements = self._index.element_count

        # Increase index size 
        if curr_elements + len(data) > max_elements:
            new_size = max(curr_elements + len(data), 2 * max_elements)
            print("New size", new_size)
            self._index.resize_index(new_size)

        self._index.add_items(data, ids, replace_deleted)
        print("Total elements in index", self._index.element_count)

    def knn_query(self, query_embedding, k = 1):
        labels, distances = self._index.knn_query(query_embedding, k)
        return labels, distances

    def get_dimension(self):
        return self._index.dim

    def get_status(self):
        print("Max elements", self._index.max_elements)
        print("Current elements", self._index.element_count)

