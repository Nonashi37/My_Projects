import sqlite3
from db import queries
from config import path_db
import os

# ✅ makedirs only once, not on every query
def init_db():
    db_dir = os.path.dirname(path_db)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)  # exist_ok avoids the extra if-check
    _execute_query(queries.task_table)
    print(f'DB connected: {path_db}')

def _execute_query(query, params=(), fetch=False):
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

def add_task(task):
    return _execute_query(queries.insert_task, (task,))

def update_task(task_id, new_task=None, completed=None):
    # ✅ Update both fields in ONE query if needed
    if new_task is not None and completed is not None:
        _execute_query(queries.update_both, (new_task, int(completed), task_id))
    elif new_task is not None:
        _execute_query(queries.update_task_text, (new_task, task_id))
    elif completed is not None:
        _execute_query(queries.update_task_completed, (int(completed), task_id))

def delete_task(task_id):
    _execute_query(queries.delete_task, (task_id,))

def get_tasks(filter_type='all'):
    # ✅ One query, dynamic WHERE clause
    filters = {
        'completed':   ' WHERE completed = 1',
        'uncompleted': ' WHERE completed = 0',
    }
    where = filters.get(filter_type, '')
    return _execute_query(queries.select_task.format(where), fetch=True)