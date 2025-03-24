"""Pydantic schemas for task and worker data validation and serialization."""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import UUID4, BaseModel


class TaskStatusEnum(str, Enum):
    """Enum representing possible task statuses."""

    PENDING = "pending"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskPriorityEnum(str, Enum):
    """Enum representing task priority levels."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# Base Task schema with common attributes
class TaskBase(BaseModel):
    """Base schema for task data with common attributes."""

    name: str
    payload: Dict[str, Any]
    priority: TaskPriorityEnum = TaskPriorityEnum.MEDIUM
    scheduled_at: Optional[datetime] = None


# Schema for creating a new task
class TaskCreate(TaskBase):
    """Schema used for creating a new task."""


# Schema for updating a task
class TaskUpdate(BaseModel):
    """Schema used for updating an existing task."""

    name: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None
    priority: Optional[TaskPriorityEnum] = None
    scheduled_at: Optional[datetime] = None
    status: Optional[TaskStatusEnum] = None


# Schema for returning a task from the API
class Task(TaskBase):
    """Schema for task data returned from the API."""

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
        """Configuration for the Task schema."""

        from_attributes = True
        json_encoders = {datetime: lambda dt: dt.isoformat(), UUID4: str}


# Worker Schemas
class WorkerBase(BaseModel):
    """Base schema for worker data."""

    name: str
    status: str = "active"


# Schema for creating a new worker
class WorkerCreate(WorkerBase):
    """Schema used for creating a new worker."""


class Worker(WorkerBase):
    """Schema for worker data returned from the API."""

    id: UUID4
    last_heartbeat: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        """Configuration for the Worker schema."""

        from_attributes = True
        json_encoders = {datetime: lambda dt: dt.isoformat(), UUID4: str}


# Schema for task list response
class TaskList(BaseModel):
    """Schema for paginated task list responses."""

    items: List[Task]
    total: int
