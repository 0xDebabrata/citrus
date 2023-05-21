import os
import sqlite3

from citrusdb.utils.utils import ensure_valid_path
from citrusdb.db.sqlite.queries import CREATE_INDEX_MANAGER_TABLE


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
            res = cur.execute(CREATE_INDEX_MANAGER_TABLE)
            res = cur.execute("SELECT name FROM sqlite_master")
            print(res.fetchone())


    def create_index(
        self,
        max_elements,
        persist_directory: str,
        M,
        ef_construction,
        allow_replace_deleted,
    ):
        self._con = sqlite3.connect(
            os.path.join(
                persist_directory, "citrus.db"
            )
        )

        cur = self._con.cursor()
        res = cur.execute("SELECT name FROM sqlite_master")
        res.fetchone()

