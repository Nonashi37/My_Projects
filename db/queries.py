task_table = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        completed INTEGER DEFAULT 0
    )
"""

insert_task = "INSERT INTO tasks (task) VALUES (?)"

# One query handles all filters — cleaner!
select_task = "SELECT id, task, completed FROM tasks{}"

update_task_text = "UPDATE tasks SET task = ? WHERE id = ?"
update_task_completed = "UPDATE tasks SET completed = ? WHERE id = ?"
update_both = "UPDATE tasks SET task = ?, completed = ? WHERE id = ?"

delete_task = "DELETE FROM tasks WHERE id = ?"

