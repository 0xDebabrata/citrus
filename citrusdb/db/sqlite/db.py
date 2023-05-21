import os
import sqlite3
from typing import Optional

from citrusdb.utils.utils import ensure_valid_path
import citrusdb.db.sqlite.queries as queries


class DB:
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

    def check_index_exists(
        self,
        name: str
    ) -> bool:
        cur = self._con.cursor()
        parameters = (name,)
        res = cur.execute(queries.GET_INDEX_BY_NAME, parameters)
        if res.fetchone() is None:
            cur.close()
            return False
        else:
            cur.close()
            return True

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
