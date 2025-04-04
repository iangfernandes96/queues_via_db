"""API endpoints for worker management."""
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.task import Worker, WorkerCreate
from app.services.worker import WorkerService

router = APIRouter()


@router.post("/", response_model=Worker, status_code=201)
async def create_worker(
    worker: WorkerCreate, db: AsyncSession = Depends(get_db)
):  # noqa
    """Create a new worker."""
    return await WorkerService.create_worker(db=db, name=worker.name)


@router.get("/{worker_id}", response_model=Worker)
async def get_worker(
    worker_id: UUID = Path(
        ..., description="The UUID of the worker to retrieve"
    ),  # noqa
    db: AsyncSession = Depends(get_db),  # noqa
):
    """Get a worker by ID."""
    db_worker = await WorkerService.get_worker(db=db, worker_id=worker_id)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker


@router.patch("/{worker_id}/heartbeat", response_model=Worker)
async def update_heartbeat(
    worker_id: UUID = Path(..., description="The UUID of the worker to update"),  # noqa
    db: AsyncSession = Depends(get_db),  # noqa
):
    """Update the heartbeat of a worker."""
    db_worker = await WorkerService.update_heartbeat(db=db, worker_id=worker_id)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker


@router.patch("/{worker_id}/status", response_model=Worker)
async def set_worker_status(
    worker_id: UUID = Path(..., description="The UUID of the worker to update"),  # noqa
    status: str = Body(..., embed=True),  # noqa
    db: AsyncSession = Depends(get_db),  # noqa
):
    """Set the status of a worker."""
    db_worker = await WorkerService.set_worker_status(
        db=db, worker_id=worker_id, status=status
    )
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker
