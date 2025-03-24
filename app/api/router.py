"""API router module for the Task Queue System.

This module configures and includes all API route endpoints for the application.
"""
from fastapi import APIRouter

from app.api.endpoints import tasks, workers

# Main API router that includes all endpoint routers
router = APIRouter()

# Include additional routers with their prefixes
router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
router.include_router(workers.router, prefix="/workers", tags=["workers"])
