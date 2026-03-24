import sqlite3
from db import queries
from config import path_db
import os

def _execute_query(query, params=(), fetch=False):
    db_dir = os.path.dirname(path_db)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    conn = sqlite3.connect(path_db)
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            return cursor.lastrowid
    finally:
        conn.close()


def init_db():
    _execute_query(queries.shopping_table)
    print(f'DB connected: {path_db}')


def add_item(item, quantity):
    return _execute_query(queries.insert_item, (item, quantity))


def mark_purchased(item_id, is_purchased):
    _execute_query(queries.update_item, (int(is_purchased), item_id))


def delete_item(item_id):
    _execute_query(queries.delete_item, (item_id,))


def get_items(filter_type):
    if filter_type == 'all':
        return _execute_query(queries.select_all, fetch=True)
    elif filter_type == 'purchased':
        return _execute_query(queries.select_purchased, fetch=True)
    elif filter_type == 'unpurchased':
        return _execute_query(queries.select_unpurchased, fetch=True)
    return[]


def get_purchased_count():
    result = _execute_query(queries.count_purchased, fetch=True)
    return result[0][0]
