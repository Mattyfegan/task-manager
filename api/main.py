import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from task_service import TaskService


class TaskCreate(BaseModel):
    title: str = Field(min_length = 1, max_length = 100)

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
    success, result = tasks.add_task(task.title)

    if not success:
        raise HTTPException(
            status_code = 400,
            detail = result
        )

    return {"message": f"task {result["title"]} has been added"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    success, result = tasks.delete_task(task_id)

    if not success:
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
    success, result = tasks.complete_task(task_id)

    if not success:
        raise HTTPException(
            status_code = 404,
            detail = result
        )

    return {"message": result}