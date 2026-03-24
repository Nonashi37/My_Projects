task_table = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        task TEXT NOT NULL,
        completed INTEGER DEFAULT 0 
    )
"""

# CRUD - CREATE - READ - UPDATE - DELETE
# INSERT SELECT UPDATE DELETE

insert_task = "INSERT INTO tasks (task) VALUES (?)"

select_task = 'SELECT id, task, completed FROM tasks'

select_task_completed = 'SELECT id, task, completed FROM tasks WHERE completed = 1'
select_task_uncompleted = 'SELECT id, task, completed FROM tasks WHERE completed = 0'

update_task = "UPDATE tasks SET task = ? WHERE id = ?"

delete_task = "DELETE FROM tasks WHERE id = ?"

delete_completed_tasks = "DELETE FROM tasks WHERE completed = 1"



