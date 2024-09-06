from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..auth.dependencies import get_current_user
from .services import TaskService
from ..auth.dependencies import User
router = APIRouter()
task_service = TaskService()

# Pydantic models for request and response validation
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str  # e.g., 'pending', 'completed'

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    status: str
    username: str
    created_at: datetime
    updated_at: datetime

# Route to create a new task
@router.post("/tasks", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user)
):
    created_task = await task_service.create_task(
        title=task.title,
        description=task.description,
        status=task.status,
        username=current_user.username
    )
    return created_task

# Route to get a specific task by ID
@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    task = await task_service.get_task(
        task_id=task_id,
        username=current_user.username,
        is_admin=current_user.role == "admin"
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you do not have permission to access it."
        )
    return task

# Route to update a specific task by ID
@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task: TaskUpdate,
    current_user: User = Depends(get_current_user)
):
    updated_task = await task_service.update_task(
        task_id=task_id,
        title=task.title,
        description=task.description,
        status=task.status,
        username=current_user.username,
        is_admin=current_user.role == "admin"
    )
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you do not have permission to update it."
        )
    return updated_task

# Route to delete a specific task by ID
@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    success = await task_service.delete_task(
        task_id=task_id,
        username=current_user.username,
        is_admin=current_user.role == "admin"
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you do not have permission to delete it."
        )

# Route to list all tasks for the current user
@router.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(current_user: User = Depends(get_current_user)):
    tasks = await task_service.list_tasks(
        username=current_user.username,
        is_admin=current_user.role == "admin"
    )
    return tasks
