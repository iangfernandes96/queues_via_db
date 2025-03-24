import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import UUID4, BaseModel, Field


class TaskStatusEnum(str, Enum):
    PENDING = "pending"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskPriorityEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


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
    id: UUID4
    status: TaskStatusEnum
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    worker_id: Optional[UUID4] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda dt: dt.isoformat(), UUID4: lambda v: str(v)}


# Worker Schemas
class WorkerBase(BaseModel):
    name: str
    status: str = "active"


class WorkerCreate(WorkerBase):
    pass


class Worker(WorkerBase):
    id: UUID4
    last_heartbeat: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda dt: dt.isoformat(), UUID4: lambda v: str(v)}


# Schema for task list response
class TaskList(BaseModel):
    items: List[Task]
    total: int
