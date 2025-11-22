CREATE_TASKS = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        time TEXT NOT NULL,
        completed INTEGER DEFAULT 0
    )
"""

INSERT_TASK = "INSERT INTO tasks (task, time) VALUES (?, ?)"

SELECT_TASK = "SELECT id, task, time, completed FROM tasks"

SELECT_COMPLETED_TASK = "SELECT id, task, time, completed FROM tasks WHERE completed = 1"

SELECT_UNCOMPLETED_TASK = "SELECT id, task, time, completed FROM tasks WHERE completed = 0"

UPDATE_TASK = "UPDATE tasks SET task = ?, time = ?, completed = ? WHERE id = ?"

UPDATE_TASK_COMPLETED = "UPDATE tasks SET completed = ? WHERE id = ?"

DELETE_TASK = "DELETE FROM tasks WHERE id = ?"
