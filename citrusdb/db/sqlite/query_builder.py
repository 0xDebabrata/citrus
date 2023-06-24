import sqlite3
from typing import Dict, List

class QueryBuilder:
    _con: sqlite3.Connection

    def __init__(self, connection):
        self._con = connection

    def build_query(self, index_name, filters):
        # Building the base SQL query
        sql_query = f"SELECT d.vector_id, d.id, d.index_id, d.text FROM index_data d JOIN index_manager m ON m.index_id = d.index_id WHERE m.name = '{index_name}'"

        # Adding the filter criteria to the SQL query
        if filters:
            sql_query += " AND "
            conditions = []
            for filter in filters:
                field = filter["field"]
                operator = filter["operator"]
                value = filter["value"]
                if isinstance(value, int) or isinstance(value, float):
                    condition = f"metadata ->> '{field}' {operator} {value}"
                else:
                    condition = f"metadata ->> '{field}' {operator} '{value}'"
                conditions.append(condition)
            sql_query += " AND ".join(conditions)

        return sql_query

    def execute_query(self, index_name: str, filters: List[Dict]):
        cursor = self._con.cursor()

        # Building and executing the query
        sql_query = self.build_query(index_name, filters)
        cursor.execute(sql_query)
        results = cursor.fetchall()

        return results

