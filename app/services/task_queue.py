from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, or_, select, update, delete
from sqlalchemy.future import select

from app.db.models import Task, TaskStatus, TaskPriority, Worker
from app.schemas.task import TaskCreate, TaskUpdate


class TaskQueueService:
    @staticmethod
    async def create_task(db: AsyncSession, task_in: TaskCreate) -> Task:
        """Create a new task in the queue."""
        db_task = Task(
            name=task_in.name,
            payload=task_in.payload,
            priority=task_in.priority,
            status=TaskStatus.SCHEDULED if task_in.scheduled_at else TaskStatus.PENDING,
            scheduled_at=task_in.scheduled_at
        )
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        return db_task

    @staticmethod
    async def get_task(db: AsyncSession, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        result = await db.execute(select(Task).filter(Task.id == task_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_tasks(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get all tasks with pagination."""
        result = await db.execute(select(Task).offset(skip).limit(limit))
        return result.scalars().all()
    
    @staticmethod
    async def get_tasks_by_status(db: AsyncSession, status: TaskStatus, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get all tasks with a specific status."""
        result = await db.execute(
            select(Task)
            .filter(Task.status == status)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    @staticmethod
    async def update_task(db: AsyncSession, task_id: int, task_in: TaskUpdate) -> Optional[Task]:
        """Update a task by ID."""
        db_task = await TaskQueueService.get_task(db, task_id)
        if not db_task:
            return None
        
        task_data = task_in.model_dump(exclude_unset=True)
        for field, value in task_data.items():
            setattr(db_task, field, value)
        
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        return db_task
    
    @staticmethod
    async def delete_task(db: AsyncSession, task_id: int) -> bool:
        """Delete a task by ID."""
        db_task = await TaskQueueService.get_task(db, task_id)
        if not db_task:
            return False
        
        await db.delete(db_task)
        await db.commit()
        return True
    
    @staticmethod
    async def pause_task(db: AsyncSession, task_id: int) -> Optional[Task]:
        """Pause a task by ID."""
        db_task = await TaskQueueService.get_task(db, task_id)
        if not db_task or db_task.status not in [TaskStatus.PENDING, TaskStatus.SCHEDULED, TaskStatus.RUNNING]:
            return None
        
        db_task.status = TaskStatus.PAUSED
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        return db_task
    
    @staticmethod
    async def resume_task(db: AsyncSession, task_id: int) -> Optional[Task]:
        """Resume a paused task by ID."""
        db_task = await TaskQueueService.get_task(db, task_id)
        if not db_task or db_task.status != TaskStatus.PAUSED:
            return None
        
        if db_task.scheduled_at and db_task.scheduled_at > datetime.utcnow():
            db_task.status = TaskStatus.SCHEDULED
        else:
            db_task.status = TaskStatus.PENDING
        
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        return db_task
    
    @staticmethod
    async def get_next_task(db: AsyncSession, worker_id: int) -> Optional[Task]:
        """Get the next task to process for a worker."""
        # Get tasks that are ready to run (PENDING or SCHEDULED with a scheduled_at time in the past)
        current_time = datetime.utcnow()
        
        stmt = (
            select(Task)
            .filter(
                or_(
                    and_(Task.status == TaskStatus.PENDING),
                    and_(
                        Task.status == TaskStatus.SCHEDULED,
                        Task.scheduled_at <= current_time
                    )
                )
            )
            .order_by(
                Task.priority.desc(),
                Task.scheduled_at.asc().nullsfirst(),
                Task.created_at.asc()
            )
            .limit(1)
            .with_for_update(skip_locked=True)
        )
        
        result = await db.execute(stmt)
        next_task = result.scalar_one_or_none()
        
        if next_task:
            next_task.status = TaskStatus.RUNNING
            next_task.started_at = current_time
            next_task.worker_id = worker_id
            db.add(next_task)
            await db.commit()
            await db.refresh(next_task)
        
        return next_task
    
    @staticmethod
    async def complete_task(db: AsyncSession, task_id: int, result: Optional[Dict[str, Any]] = None) -> Optional[Task]:
        """Mark a task as completed with an optional result."""
        db_task = await TaskQueueService.get_task(db, task_id)
        if not db_task or db_task.status != TaskStatus.RUNNING:
            return None
        
        db_task.status = TaskStatus.COMPLETED
        db_task.completed_at = datetime.utcnow()
        db_task.result = result
        
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        return db_task
    
    @staticmethod
    async def fail_task(db: AsyncSession, task_id: int, error: str) -> Optional[Task]:
        """Mark a task as failed with an error message."""
        db_task = await TaskQueueService.get_task(db, task_id)
        if not db_task or db_task.status != TaskStatus.RUNNING:
            return None
        
        db_task.status = TaskStatus.FAILED
        db_task.completed_at = datetime.utcnow()
        db_task.error = error
        
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        return db_task 