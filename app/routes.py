from fastapi import APIRouter, HTTPException
from app.models import TaskCreate

from app.database import get_connection

router = APIRouter()


@router.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/tasks")
def get_tasks():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "id": row["id"],
            "title": row["title"],
            "completed": bool(row["completed"])
        }
        for row in rows
    ]


@router.get("/tasks/{task_id}")
def get_task(task_id: int):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "id": row["id"],
        "title": row["title"],
        "completed": bool(row["completed"])
    }

@router.post("/tasks", status_code=201)
def create_task(task: TaskCreate):

    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tasks(title, completed)
        VALUES (?, ?)
        """,
        (task.title, task.completed)
    )

    task_id = cursor.lastrowid

    conn.commit()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    row = cursor.fetchone()

    conn.close()

    return {
        "id": row["id"],
        "title": row["title"],
        "completed": bool(row["completed"])
    }