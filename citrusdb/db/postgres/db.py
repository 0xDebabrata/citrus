import psycopg
from psycopg_pool import ConnectionPool
from typing import Dict, List, Optional, Tuple
from citrusdb.db import BaseDB
from citrusdb.utils.utils import ensure_valid_path
import citrusdb.db.postgres.queries as queries
from citrusdb.db.postgres.query_builder import QueryBuilder


class PostgresDB(BaseDB):
    _pool: ConnectionPool

    def __init__(
        self,
        connection_string: str
    ):
        # Setup connection pool
        self._pool = ConnectionPool(connection_string)

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
        ids: List[int]
    ):
        """
        Delete vectors with given list of IDs from specific index

        index_id: ID of index where the elements belong
        ids: List of IDs to be deleted
        """
        parameters = (tuple(ids), index_id)
        with self._pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(queries.DELETE_VECTORS_FROM_INDEX, parameters)
                conn.commit()

    def filter_vectors(self, index_name: str, filters: List[Dict]):
        query_builder = QueryBuilder(self._con)
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

    def insert_to_index(
        self,
        data
    ):
        cur = self._con.cursor()
        cur.executemany(queries.INSERT_DATA_TO_INDEX, data)
        self._con.commit()
        cur.close()

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
