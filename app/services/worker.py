"""Worker service module for handling worker-related database operations.

This module provides methods for managing worker entities, including
creating, retrieving, and updating worker records in the database.
"""
from datetime import datetime, timezone
from typing import Optional, Sequence, Union
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Worker
from app.schemas.task import WorkerCreate

# Import our stub for better typing
from app.services.sa_types import select


class WorkerService:
    """Service class for managing workers in the task queue system.

    Provides methods for creating workers, retrieving worker information,
    updating heartbeats, and managing worker status.
    """

    @staticmethod
    async def create_worker(db: AsyncSession, worker_in: WorkerCreate) -> Worker:
        """Create a new worker in the database."""
        now = datetime.now(timezone.utc)
        db_worker = Worker(
            name=worker_in.name,
            status=worker_in.status,
            last_heartbeat=now,
            created_at=now,
            updated_at=now,
        )
        db.add(db_worker)
        await db.commit()
        await db.refresh(db_worker)
        return db_worker

    @staticmethod
    async def get_worker(
        db: AsyncSession, worker_id: Union[str, UUID]
    ) -> Optional[Worker]:
        """Get a worker by ID."""
        result = await db.execute(select(Worker).filter(Worker.id == worker_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_workers(
        db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> Sequence[Worker]:
        """Get all workers with pagination."""
        result = await db.execute(select(Worker).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def update_heartbeat(
        db: AsyncSession, worker_id: Union[str, UUID]
    ) -> Optional[Worker]:
        """Update a worker's heartbeat timestamp."""
        worker = await WorkerService.get_worker(db, worker_id)
        if not worker:
            return None

        now = datetime.now(timezone.utc)
        # Update the worker's heartbeat time
        worker.last_heartbeat = now
        worker.updated_at = now

        db.add(worker)
        await db.commit()
        await db.refresh(worker)
        return worker

    @staticmethod
    async def set_worker_status(
        db: AsyncSession, worker_id: Union[str, UUID], status: str
    ) -> Optional[Worker]:
        """Set a worker's status."""
        worker = await WorkerService.get_worker(db, worker_id)
        if not worker:
            return None

        now = datetime.now(timezone.utc)
        # Update the worker's status and updated_at time
        worker.status = status
        worker.updated_at = now

        db.add(worker)
        await db.commit()
        await db.refresh(worker)
        return worker
