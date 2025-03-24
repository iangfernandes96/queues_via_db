from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models import Worker


class WorkerService:
    @staticmethod
    async def create_worker(db: AsyncSession, name: str) -> Worker:
        """Create a new worker."""
        db_worker = Worker(
            name=name,
            status="active",
            last_heartbeat=datetime.utcnow()
        )
        db.add(db_worker)
        await db.commit()
        await db.refresh(db_worker)
        return db_worker

    @staticmethod
    async def get_worker(db: AsyncSession, worker_id: int) -> Optional[Worker]:
        """Get a worker by ID."""
        result = await db.execute(select(Worker).filter(Worker.id == worker_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_heartbeat(db: AsyncSession, worker_id: int) -> Optional[Worker]:
        """Update the last heartbeat time of a worker."""
        db_worker = await WorkerService.get_worker(db, worker_id)
        if not db_worker:
            return None
        
        db_worker.last_heartbeat = datetime.utcnow()
        db.add(db_worker)
        await db.commit()
        await db.refresh(db_worker)
        return db_worker
    
    @staticmethod
    async def set_worker_status(db: AsyncSession, worker_id: int, status: str) -> Optional[Worker]:
        """Set the status of a worker."""
        db_worker = await WorkerService.get_worker(db, worker_id)
        if not db_worker:
            return None
        
        db_worker.status = status
        db.add(db_worker)
        await db.commit()
        await db.refresh(db_worker)
        return db_worker 