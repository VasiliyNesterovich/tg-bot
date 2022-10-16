import os
from typing import Dict, List, Tuple

import sqlite3
import buffer



# conn = sqlite3.connect(os.path.join("db", f"{user_id}.db"))
# cursor = conn.cursor()




def insert(table: str, column_values: Dict):
    conn = sqlite3.connect(os.path.join("db", f"{buffer.user_id}.db"))
    cursor = conn.cursor()

    columns = ', '.join( column_values.keys() )
    values = [tuple(column_values.values())]
    placeholders = ", ".join( "?" * len(column_values.keys()) )
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()
    conn.close()


def fetchall(table: str, columns: List[str]) -> List[Tuple]:
    conn = sqlite3.connect(os.path.join("db", f"{buffer.user_id}.db"))
    cursor = conn.cursor()

    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    conn.close()
    return result


def delete(table: str, row_id: int) -> None:
    conn = sqlite3.connect(os.path.join("db", f"{buffer.user_id}.db"))
    cursor = conn.cursor()

    row_id = int(row_id)
    cursor.execute(f"delete from {table} where id={row_id}")
    conn.commit()
    conn.close()


def get_cursor():
    conn = sqlite3.connect(os.path.join("db", f"{buffer.user_id}.db"))
    cursor = conn.cursor()
    return cursor


def _init_db():
    """Инициализирует БД"""
    conn = sqlite3.connect(os.path.join("db", f"{buffer.user_id}.db"))
    cursor = conn.cursor()

    with open("createdb.sql", "r", encoding='utf-8') as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()
    conn.close()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    conn = sqlite3.connect(os.path.join("db", f"{buffer.user_id}.db"))
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='expense'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    conn.close()
    _init_db()

check_db_exists()
