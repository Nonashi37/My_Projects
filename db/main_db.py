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
        conn.close() # Обязательно закрываем соединение!

def init_db():
    _execute_query(queries.task_table)
    print(f'БД подключена по пути: {path_db}')

def add_task(task):
    return _execute_query(queries.insert_task, (task,))

def update_task(task_id, new_task=None, completed=None):
    if new_task is not None:
        _execute_query(queries.update_task, (new_task, task_id))
    if completed is not None:
        _execute_query("UPDATE tasks SET completed = ? WHERE id = ?", (int(completed), task_id))

def delete_task(task_id):
    _execute_query(queries.delete_task, (task_id,))

def get_tasks(filter_type):
    if filter_type == 'all':
        return _execute_query(queries.select_task, fetch=True)
    elif filter_type == 'completed':
        return _execute_query(queries.select_task_completed, fetch=True)
    elif filter_type == 'uncompleted':
        return _execute_query(queries.select_task_uncompleted, fetch=True)
    return []


def delete_completed_tasks():
    return _execute_query(queries.delete_completed_tasks)
