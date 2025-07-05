from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4, UUID

app = FastAPI(
    title="Crud Task API",
    description="A simple API for managing tasks",
    version="0.1.0",
)

class Task(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

tasks_db: List[Task] = []

@app.post("/tasks/", response_model=Task, status_code=status.HTTP_201_CREATED,tags=["tasks"], summary="Create a new task")
def create_task(task: Task):
    task.id = uuid4()
    if any(t.title == task.title for t in tasks_db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task with this title already exists")
    tasks_db.append(task)
    return task

@app.get("/tasks/", response_model=List[Task], tags=["tasks"])
def read_tasks():
    return tasks_db

@app.get("/tasks/{task_id}", response_model=Task, tags=["tasks"])
def read_task(task_id: UUID):
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task, tags=["tasks"])
def update_task(task_id: UUID, updated_task: Task):
    for idx, task in enumerate(tasks_db):
        if task.id == task_id:
            updated_task.id = task_id
            tasks_db[idx] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", response_model=Task, tags=["tasks"])
def delete_task(task_id: UUID):
    for idx, task in enumerate(tasks_db):
        if task.id == task_id:
            return tasks_db.pop(idx)
    raise HTTPException(status_code=404, detail="Task not found")

@app.patch("/tasks/{task_id}/toggle", response_model=Task, tags=["tasks"])
def toggle_task(task_id: UUID):
    for task in tasks_db:
        if task.id == task_id:
            task.completed = not task.completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.get("/tasks/completed/", response_model=List[Task], tags=["tasks"])
def get_completed_tasks():
    return [task for task in tasks_db if task.completed]

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to the Task API"}