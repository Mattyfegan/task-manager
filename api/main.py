import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ``task_service`` lives in the repository root, one level above this file.
# Put that root on the path so the app imports whether it is started from the
# repository root (``uvicorn api.main:app``) or from inside ``api/``
# (``uvicorn main:app``).
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from task_service import TaskService


class TaskCreate(BaseModel):
    title: str

app = FastAPI()

tasks = TaskService([
    {"id": 1, "title": "Learn FastAPI", "completed": False},
    {"id": 2, "title": "Understand HTTP", "completed": True}
])
# find_task, add_task, delete_task, complete_task

@app.get("/health")
def health_check():
    return {"status" : "healthy"}

@app.get("/tasks")
def get_tasks():
    return tasks.tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = tasks.find_task(task_id)

    if task is None:
        raise HTTPException(
            status_code = 404,
            detail = "Task not found"
        )

    return task

@app.post("/tasks", status_code=201)
def add_task(task : TaskCreate):
    result = tasks.add_task(task.title)

    if result == "Invalid title!" or result == "Title is too long!":
        raise HTTPException(
            status_code = 400,
            detail = result
        )

    return {"message": result}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    result = tasks.delete_task(task_id)

    if result == "Task not found":
        raise HTTPException(
            status_code = 404,
            detail = result
        )

    return {"message" : result}

@app.delete("/tasks")
def delete_all_tasks():
    return {"message" : tasks.delete_task(None, True)}


@app.patch("/tasks/{task_id}")
def complete_task(task_id: int):
    result = tasks.complete_task(task_id)

    if result == f'Task id {task_id} not found':
        raise HTTPException(
            status_code = 404,
            detail = result
        )

    if result == f'Task {task_id} is already completed':
        raise HTTPException(
            status_code = 409,
            detail = result
        )

    return {"message": result}