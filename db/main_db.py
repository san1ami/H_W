import sqlite3
from db import querles
from config import path_db
from typing import Any
from datetime import datetime

def init_db() -> None:
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(querles.CREATE_TASKS)
    print("База данных успешно инициализирована!")
    conn.commit()
    conn.close()

def add_task(task: str | None, time: str) -> int:
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(querles.INSERT_TASK, (task, time))
    conn.commit()
    task_id = cursor.rowcount
    conn.close()
    return task_id

def get_tasks(filter_type: str) -> list:
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    if filter_type == "completed":
        cursor.execute(querles.SELECT_COMPLETED_TASK)
    elif filter_type == "uncompleted":
        cursor.execute(querles.SELECT_UNCOMPLETED_TASK)
    else:
        cursor.execute(querles.SELECT_TASK)

    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task(id: int, task: str | None = None , completed: int | None = None, time: str | None = None) -> None:
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    if task is not None:
        cursor.execute(querles.UPDATE_TASK, (task, time, id))

    if completed is not None:
        cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, id))
    
    conn.commit()
    conn.close()

def delete_task(id: int) -> None:
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(querles.DELETE_TASK, (id, ))
    conn.commit()
    conn.close()
