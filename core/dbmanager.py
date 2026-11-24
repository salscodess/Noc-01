import asyncio
import sqlite3
import time

def dump_database(database):
    data = {}

    with sqlite3.connect(database) as db:
        cursor = db.cursor()

        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type = 'table'
        """)

        tables = cursor.fetchall()

        for (table_name,) in tables:
            cursor.execute(f'SELECT * FROM "{table_name}"')

            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()

            data[table_name] = [
                dict(zip(columns, row))
                for row in rows
            ]

    return data
# Universal database query
def query_dev(db, sql, params=()):
    with sqlite3.connect(db) as connection:
        cursor = connection.execute(sql, params)

        if cursor.description:
            return cursor.fetchall()

        return cursor.rowcount