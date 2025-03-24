from datetime import datetime
from typing import Any, Dict, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum


class TaskStatusEnum(str, Enum):
    PENDING = "pending"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskPriorityEnum(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


# Base Task schema with common attributes
class TaskBase(BaseModel):
    name: str
    payload: Dict[str, Any]
    priority: TaskPriorityEnum = TaskPriorityEnum.MEDIUM
    scheduled_at: Optional[datetime] = None


# Schema for creating a new task
class TaskCreate(TaskBase):
    pass


# Schema for updating a task
class TaskUpdate(BaseModel):
    name: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None
    priority: Optional[TaskPriorityEnum] = None
    scheduled_at: Optional[datetime] = None
    status: Optional[TaskStatusEnum] = None


# Schema for returning a task from the API
class Task(TaskBase):
    id: int
    status: TaskStatusEnum
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    worker_id: Optional[int] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    class Config:
        from_attributes = True


# Worker Schemas
class WorkerBase(BaseModel):
    name: str
    status: str = "active"


class WorkerCreate(WorkerBase):
    pass


class Worker(WorkerBase):
    id: int
    last_heartbeat: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 