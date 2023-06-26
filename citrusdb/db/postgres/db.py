from psycopg_pool import ConnectionPool
from psycopg import sql
from typing import Any, Dict, List, Optional, Tuple
from citrusdb.db import BaseDB
import citrusdb.db.postgres.queries as queries
from citrusdb.db.postgres.query_builder import QueryBuilder
from citrusdb.utils.types import IDs
from citrusdb.utils.utils import convert_row_to_dict


class PostgresDB(BaseDB):
    _pool: ConnectionPool

    def __init__(
        self,
        **kwargs: Dict[str, Any]
    ):
        # Setup connection pool
        self._pool = ConnectionPool(kwargs=kwargs)

        # Create index_manager and index_data table if they don't exist already
        with self._pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(queries.CREATE_INDEX_MANAGER_TABLE)
                cur.execute(queries.CREATE_INDEX_DATA_TABLE)
                conn.commit()

    def create_index(
        self,
        name: str,
        max_elements: int,
        M: int,
        ef_construction: int,
        allow_replace_deleted: bool,
        dimensions: Optional[int] = 1536,
    ):
        ef = ef_construction
        parameters = (name, dimensions, max_elements, M, ef, ef_construction, allow_replace_deleted)
        # Create new index entry to postgres db
        with self._pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(queries.INSERT_INDEX_TO_MANAGER, parameters)
                conn.commit()

    def delete_vectors_from_index(
        self,
        index_id: int,
        ids: IDs
    ):
        """
        Delete vectors with given list of IDs from specific index

        index_id: ID of index where the elements belong
        ids: List of IDs to be deleted
        """

        vector_ids = []
        parameters = [ids, index_id]
        with self._pool.connection() as conn:
            with conn.cursor() as cur:
                for vector_id in cur.execute(queries.DELETE_VECTORS_FROM_INDEX, parameters):
                    vector_ids.append(vector_id)
                conn.commit()

        return vector_ids

    def filter_vectors(self, index_name: str, filters: List[Dict]):
        """
        Get list of IDs of vectors that match filters.

        index_name: Name of index where the elements belong
        filters: List of filters to be applied
        """

        with self._pool.connection() as conn:
            query_builder = QueryBuilder(conn)
            res = query_builder.execute_query(index_name, filters)
            allowed_ids = []
            for row in res:
                allowed_ids.append(row[0])
            return allowed_ids

    def get_indices(self):
        """
        Get all index details
        """
        with self._pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(queries.GET_ALL_INDEX_DETAILS)
                return cur.fetchall()

    def get_index_details(
        self,
        name: str
    ) -> Optional[Tuple[int, str, int, int, int, int, int, bool]]:
        """
        Get specific index details

        name: Name of index to fetch
        """
        parameters = (name,)
        with self._pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(queries.GET_INDEX_DETAILS_BY_NAME, parameters)
                return cur.fetchone()

    def get_vector_ids_of_results(
        self,
        name: str,
        results: List[List[int]],
        include: Dict
    ):
        """
        Get user facing IDs of results

        name: Name of index
        results: List of list of integer HNSW labels
        """
        index_details = self.get_index_details(name)
        if not(index_details):
            return

        cols = [sql.Identifier("id")]
        if include["document"]:
            cols.append(sql.Identifier("text"))
            if include["metadata"]:
                cols.append(sql.Identifier("metadata"))
        elif include["metadata"]:
            cols.append(sql.Identifier("metadata"))

        returning_list = []
        unordered_rows_list = []
        index_id = index_details[0]

        with self._pool.connection() as conn:
            with conn.cursor() as cur:
                data = []
                for ids in results:
                    ids_list = []
                    for id in ids:
                        ids_list.append(int(id))
                    data.append([ids_list, index_id])

                query = sql.SQL(queries.GET_VECTOR_IDS_OF_RESULTS).format(
                    sql.SQL(", ").join(cols)
                )
                cur.executemany(
                    query,
                    data,
                    returning=True
                )
                while True:
                    rows = cur.fetchall()
                    unordered_rows_list.append(rows)
                    if not cur.nextset():
                        break;

                conn.commit()

        # Order rows according to order of id in ids list
        for i, ids in enumerate(results):
            unordered_rows = unordered_rows_list[i]
            ordered_rows = []
            for id in ids:
                low = 0; high = len(unordered_rows) - 1
                while (low <= high):
                    mid = low + (high - low)//2
                    curr_vector_id = unordered_rows[mid][0]
                    if curr_vector_id == id:
                        ordered_rows.append(
                            convert_row_to_dict(
                                row=unordered_rows[mid],
                                include=include
                            )
                        )
                        break
                    elif curr_vector_id < id:
                        low = mid + 1
                    else:
                        high = mid - 1

            returning_list.append(ordered_rows)
        return returning_list

    def insert_to_index(
        self,
        data
    ):
        """
        Insert vectors to index

        data: Tuple of tuples corresponding to each row
        """
        vector_ids = []
        with self._pool.connection() as conn:
            with conn.cursor() as cur:
                cur.executemany(queries.INSERT_DATA_TO_INDEX, data, returning=True)
                while True:
                    vector_ids.append(cur.fetchone()[0])        # type: ignore
                    if not cur.nextset():
                        break;

                conn.commit()

        return vector_ids

    def update_ef(
        self,
        name: str,
        ef: int
    ):
        """
        Update ef for an index

        name: Name of index to be updated
        ef: New ef value
        """
        parameters = (ef, name)
        with self._pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(queries.UPDATE_EF, parameters)
                conn.commit()
