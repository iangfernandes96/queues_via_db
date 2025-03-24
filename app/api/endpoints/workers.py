from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.task import Worker, WorkerCreate
from app.services.worker import WorkerService

router = APIRouter()


@router.post("/", response_model=Worker, status_code=201)
async def create_worker(worker: WorkerCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new worker.
    """
    return await WorkerService.create_worker(db=db, name=worker.name)


@router.get("/{worker_id}", response_model=Worker)
async def get_worker(worker_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a worker by ID.
    """
    db_worker = await WorkerService.get_worker(db=db, worker_id=worker_id)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker


@router.patch("/{worker_id}/heartbeat", response_model=Worker)
async def update_heartbeat(worker_id: int, db: AsyncSession = Depends(get_db)):
    """
    Update the heartbeat of a worker.
    """
    db_worker = await WorkerService.update_heartbeat(db=db, worker_id=worker_id)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker


@router.patch("/{worker_id}/status", response_model=Worker)
async def set_worker_status(
    worker_id: int, 
    status: str = Body(..., embed=True), 
    db: AsyncSession = Depends(get_db)
):
    """
    Set the status of a worker.
    """
    db_worker = await WorkerService.set_worker_status(db=db, worker_id=worker_id, status=status)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker 