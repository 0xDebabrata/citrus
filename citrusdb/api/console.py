import os
from typing import Any, Dict, Optional
import shutil

from citrusdb.api.index import Index
from citrusdb.db import BaseDB
#from citrusdb.db.postgres.db import PostgresDB
from citrusdb.db.sqlite.db import SQLiteDB


class ConsoleAPI:
    _db: Dict[str, Index] 
    _SQLClient: BaseDB
    persist_directory: Optional[str]
    _TEMP_DIRECTORY = "citrus_temp"

    def __init__(
        self,
        persist_directory: Optional[str] = None,
        database_type: Optional[str] = "sqlite",
        **kwargs: Optional[Dict[str, Any]]
    ):
        self._db = {}
        self.persist_directory = persist_directory

        if not(persist_directory) and os.path.isdir(self._TEMP_DIRECTORY):
            # Cleanup previous sqlite data
            shutil.rmtree(self._TEMP_DIRECTORY)

        # TODO: Add postgres support to console
        '''
        if persist_directory and (database_type == "pg" or database_type == "postgres"):
            self._SQLClient = PostgresDB(**kwargs)
        else:
        '''
        self._SQLClient = SQLiteDB(persist_directory if persist_directory else self._TEMP_DIRECTORY)

    def get_all_indices(self):
        '''
        Get information for all indices
        '''

        return self._SQLClient.get_indices()
