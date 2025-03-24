from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import TaskStatus
from app.schemas.task import Task, TaskCreate, TaskList, TaskUpdate
from app.services.task_queue import TaskQueueService

router = APIRouter()


@router.post("/", response_model=Task, status_code=201)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new task in the queue.
    """
    return await TaskQueueService.create_task(db=db, task_in=task)


@router.get("/", response_model=TaskList)
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = Query(None, description="Filter tasks by status"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get all tasks with pagination and optional status filtering.
    """
    if status:
        try:
            task_status = TaskStatus[status.upper()]
            tasks = await TaskQueueService.get_tasks_by_status(
                db=db, status=task_status, skip=skip, limit=limit
            )
            total = len(
                tasks
            )  # This is a simplification; in production, do a count query
            return {"items": tasks, "total": total}
        except KeyError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")

    tasks = await TaskQueueService.get_tasks(db=db, skip=skip, limit=limit)
    total = await TaskQueueService.get_tasks_count(db=db)
    return {"items": tasks, "total": total}


@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: UUID = Path(..., description="The UUID of the task to retrieve"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get a task by ID.
    """
    db_task = await TaskQueueService.get_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.put("/{task_id}", response_model=Task)
async def update_task(
    task: TaskUpdate,
    task_id: UUID = Path(..., description="The UUID of the task to update"),
    db: AsyncSession = Depends(get_db),
):
    """
    Update a task by ID.
    """
    db_task = await TaskQueueService.update_task(db=db, task_id=task_id, task_in=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: UUID = Path(..., description="The UUID of the task to delete"),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a task by ID.
    """
    success = await TaskQueueService.delete_task(db=db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None


@router.patch("/{task_id}/pause", response_model=Task)
async def pause_task(
    task_id: UUID = Path(..., description="The UUID of the task to pause"),
    db: AsyncSession = Depends(get_db),
):
    """
    Pause a task by ID.
    """
    db_task = await TaskQueueService.pause_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found or cannot be paused (must be in PENDING, SCHEDULED, or RUNNING state)",
        )
    return db_task


@router.patch("/{task_id}/resume", response_model=Task)
async def resume_task(
    task_id: UUID = Path(..., description="The UUID of the task to resume"),
    db: AsyncSession = Depends(get_db),
):
    """
    Resume a paused task by ID.
    """
    db_task = await TaskQueueService.resume_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found or cannot be resumed (must be in PAUSED state)",
        )
    return db_task
