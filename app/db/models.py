"""Database models for the Task Queue System.

This module defines the database models for the Task Queue System.
"""
import enum
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import JSON, Column, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base


class TaskStatus(enum.Enum):
    """Enum for task status."""

    PENDING = "pending"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskPriority(enum.Enum):
    """Enum for task priority."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


def generate_uuid() -> str:
    """Generate a UUID as string."""
    return str(uuid.uuid4())


class Task(Base):
    """Task model."""

    # Allow non-Mapped type annotations
    __allow_unmapped__ = True

    __tablename__ = "tasks"

    id = Column(
        UUID(as_uuid=False), primary_key=True, default=generate_uuid, index=True
    )
    name = Column(String(255), nullable=False)
    payload = Column(JSON, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    priority = Column(String(20), default=TaskPriority.MEDIUM.name, nullable=False)
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(),
        onupdate=lambda: datetime.now(),
        nullable=False,
    )
    worker_id = Column(UUID(as_uuid=False), ForeignKey("workers.id"), nullable=True)
    result = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)

    # Relationship to Worker with type annotation
    worker: Any = relationship("Worker", back_populates="tasks")


class Worker(Base):
    """Worker model."""

    # Allow non-Mapped type annotations
    __allow_unmapped__ = True

    __tablename__ = "workers"

    id = Column(
        UUID(as_uuid=False), primary_key=True, default=generate_uuid, index=True
    )
    name = Column(String(255), nullable=False)
    status = Column(String(50), default="active", nullable=False)
    last_heartbeat = Column(
        DateTime(timezone=True), default=lambda: datetime.now(), nullable=False
    )
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(),
        onupdate=lambda: datetime.now(),
        nullable=False,
    )

    # Relationship to Task with type annotation
    tasks: Any = relationship("Task", back_populates="worker")
