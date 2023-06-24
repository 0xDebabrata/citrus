import os
import sqlite3
from typing import Dict, List, Optional, Tuple

from citrusdb.db import BaseDB
from citrusdb.utils.types import IDs
from citrusdb.utils.utils import ensure_valid_path
import citrusdb.db.sqlite.queries as queries
from citrusdb.db.sqlite.query_builder import QueryBuilder


class SQLiteDB(BaseDB):
    _con: sqlite3.Connection

    def __init__(
        self,
        persist_directory: str,
    ):
        ensure_valid_path(persist_directory)

        self._con = sqlite3.connect(
            os.path.join(
                persist_directory, "citrus.db"
            )
        )

        cur = self._con.cursor()
        cur.execute("PRAGMA foreign_keys = ON")    # Enable foreign keys
        cur.executescript(f'''
        BEGIN;
        {queries.CREATE_INDEX_MANAGER_TABLE}
        {queries.CREATE_INDEX_DATA_TABLE}
        END;
        ''')
        cur.close()

    def create_index(
        self,
        name: str,
        max_elements: int,
        M: int,
        ef_construction: int,
        allow_replace_deleted: bool,
        dimensions: Optional[int] = 1536,
    ):
        cur = self._con.cursor()
        ef = ef_construction
        parameters = (name, dimensions, max_elements, M, ef, ef_construction, allow_replace_deleted)
        cur.execute(queries.INSERT_INDEX_TO_MANAGER, parameters)
        self._con.commit()
        cur.close()

    def delete_vectors_from_index(
        self,
        index_id: int,
        ids: IDs
    ):
        cur = self._con.cursor()
        query = queries.DELETE_VECTORS_FROM_INDEX.format(", ".join("?" * len(ids)))
        parameters = tuple(ids) + (index_id,)
        cur.execute(query, parameters)

        rows = cur.fetchall()
        self._con.commit()
        cur.close()

        vector_ids = [row[0] for row in rows]
        return vector_ids

    def filter_vectors(self, index_name: str, filters: List[Dict]):
        query_builder = QueryBuilder(self._con)
        res = query_builder.execute_query(index_name, filters)
        allowed_ids = []
        for row in res:
            allowed_ids.append(row[0])
        return allowed_ids

    def get_indices(self):
        """
        Fetch all index details from index_manager table.
        Returns a list of tuples where each one corresponds to an index.
        """

        cur = self._con.cursor()
        res = cur.execute(queries.GET_ALL_INDEX_DETAILS)
        rows = res.fetchall()
        cur.close()
        return rows

    def get_index_details(
        self,
        name: str
    ) -> Optional[Tuple[int, str, int, int, int, int, int, bool]]:
        cur = self._con.cursor()
        parameters = (name,)
        res = cur.execute(queries.GET_INDEX_DETAILS_BY_NAME, parameters)
        row = res.fetchone()
        cur.close()
        return row

    def get_vector_ids_of_results(
        self,
        name: str,
        results: List[List[int]]
    ) -> List[IDs]:
        lolo_vector_ids = []
        index_details = self.get_index_details(name)
        index_id = index_details[0]               # type: ignore

        cur = self._con.cursor()
        for ids in results:
            query = queries.GET_VECTOR_IDS_OF_RESULTS.format(", ".join("?" * len(ids)))
            parameters = ()
            for id in ids:
                parameters += (int(id),)
            parameters += (index_id,)
            res = cur.execute(query, parameters)
            rows = res.fetchall()
            lolo_vector_ids.append([row[0] for row in rows])
        cur.close()

        return lolo_vector_ids

    def insert_to_index(
        self,
        data
    ):
        cur = self._con.cursor()
        vector_ids = []
        for row in data:
            res = cur.execute(queries.INSERT_DATA_TO_INDEX, row)
            vector_ids.append(res.fetchone()[0])

        self._con.commit()
        cur.close()

        return vector_ids

    def update_ef(
        self,
        name: str,
        ef: int
    ):
        cur = self._con.cursor()
        parameters = (ef, name)
        cur.execute(queries.UPDATE_EF, parameters)
        self._con.commit()
        cur.close()
