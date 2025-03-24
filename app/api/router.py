from fastapi import APIRouter

from app.api.endpoints import tasks, workers

api_router = APIRouter()

# Include all API endpoints
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(workers.router, prefix="/workers", tags=["workers"])
