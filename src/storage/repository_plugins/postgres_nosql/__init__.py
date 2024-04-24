import json

import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from common.utils.encryption import decrypt
from storage.repository_interface import RepositoryInterface

class Repository(RepositoryInterface):
    def __init__(
        self,
        username: str,
        password: str,
        host: str,
        database: str,
        tls: bool = False,
        port: int = 5432,
        **kwargs,
    ):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=database,
            user=username,
            password=decrypt(password),
            sslmode='require' if tls else 'disable'
        )
        self.table = database
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)


        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {database} (_id TEXT PRIMARY KEY, json_document JSONB)")
        self.conn.commit()

    def get(self, uid: str) -> dict:
        self.cursor.execute(sql.SQL("SELECT * FROM data_modelling WHERE _id = %s"), (uid,))
        result = self.cursor.fetchone()
        return result

    def add(self, uid: str, document: dict) -> bool:
       raise NotImplementedError

    def update(self, uid: str, document: dict) -> bool:
        try:

            # Prepare the SQL UPDATE statement
            update_query = f"UPDATE {self.table} SET json_document = %s WHERE _id LIKE %s"

            # Execute the UPDATE statement
            self.cursor.execute(
                sql.SQL("UPDATE {} SET json_document = %s WHERE _id LIKE %s")
                .format(sql.Identifier(self.table)),
                [json.dumps(document), uid])

            # Commit the changes
            self.conn.commit()
            return True
        except psycopg2.Error as ex:
            self.conn.rollback()
            raise ex

    def delete(self, uid: str) -> bool:
        self.cursor.execute("DELETE FROM %s WHERE _id = %s", (self.table, uid,))
        self.conn.commit()
        return True

    def find(self, filters: dict) -> list[dict] | None:
        query = f"SELECT '{json.dumps(filters)}' FROM {self.table} "
        # query += f" WHERE jsonb_field->>'name' = %s"
        # query += " AND ".join([f"{key} = %s" for key in filters.keys()])
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        print(res)
        return res

    def find_one(self, filters: dict) -> dict | None:
        raise NotImplementedError()

    def update_blob(self, uid: str, blob: bytearray):
        raise NotImplementedError

    def get_blob(self, uid: str) -> bytearray:
        raise NotImplementedError

    def delete_blob(self, uid: str) -> bool:
        raise NotImplementedError



