from psycopg import Connection, sql
from typing import Dict, List

class QueryBuilder:
    _con: Connection

    def __init__(self, connection):
        self._con = connection

    def build_query(self, filters):
        # Building the base SQL query
        sql_query = f"SELECT d.id, d.index_id, d.text FROM index_data d JOIN index_manager m ON m.index_id = d.index_id WHERE m.name = %s"

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

        return sql.SQL(sql_query)

    def execute_query(self, index_name: str, filters: List[Dict]):
        with self._con.cursor() as cur:
            # Building and executing the query
            sql_query = self.build_query(filters)
            parameters = (index_name,)
            cur.execute(sql_query, parameters)
            return cur.fetchall()

