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
        res = cur.execute("SELECT name FROM sqlite_master")
        if res.fetchone() is None:
            res = cur.execute(queries.CREATE_INDEX_MANAGER_TABLE)
            res = cur.execute("SELECT name FROM sqlite_master")

    def check_index_exists(
        self,
        name: str
    ) -> bool:
        cur = self._con.cursor()
        parameters = (name,)
        res = cur.execute(queries.GET_INDEX_BY_NAME, parameters)
        index = res.fetchone()
        if index is None:
            return False
        else:
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
        cur.execute(queries.CREATE_INDEX, parameters)
        self._con.commit()

