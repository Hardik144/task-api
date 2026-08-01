from fastapi import APIRouter, HTTPException, Response
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

    cursor.execute("SELECT * FROM tasks ORDER BY id;")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "completed": row[2]
        }
        for row in rows
    ]


@router.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s;",
        (task_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "id": row[0],
        "title": row[1],
        "completed": row[2]
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
        INSERT INTO tasks (title, completed)
        VALUES (%s, %s)
        RETURNING *;
        """,
        (task.title, task.completed)
    )

    row = cursor.fetchone()

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "id": row[0],
        "title": row[1],
        "completed": row[2]
    }


@router.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskCreate):

    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET title = %s,
            completed = %s
        WHERE id = %s
        RETURNING *;
        """,
        (task.title, task.completed, task_id)
    )

    row = cursor.fetchone()

    if row is None:
        conn.rollback()
        cursor.close()
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "id": row[0],
        "title": row[1],
        "completed": row[2]
    }


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM tasks
        WHERE id = %s
        RETURNING id;
        """,
        (task_id,)
    )

    row = cursor.fetchone()

    if row is None:
        conn.rollback()
        cursor.close()
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    conn.commit()

    cursor.close()
    conn.close()

    return Response(status_code=204)