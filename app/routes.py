from fastapi import APIRouter, HTTPException

from app.models import TaskCreate
from app.data import tasks

router = APIRouter()


@router.get("/")
def root():
    return {"message": "Welcome to the Task API!"}


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.get("/tasks")
def get_tasks():
    return tasks


@router.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(status_code=404, detail="Task not found")


@router.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "completed": task.completed
    }

    tasks.append(new_task)
    return new_task


@router.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskCreate):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["completed"] = updated_task.completed
            return task

    raise HTTPException(status_code=404, detail="Task not found")


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted successfully"}

    raise HTTPException(status_code=404, detail="Task not found")