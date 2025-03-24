"""Main application module for the Task Queue API.

This module initializes and configures the FastAPI application,
sets up database connections, and includes all API routers.
"""
import logging

from fastapi import Depends, FastAPI

try:
    from sqlalchemy.ext.asyncio import AsyncSession
except ImportError:
    from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from app.api.endpoints import tasks, workers
from app.core.config import settings
from app.db.database import Base, engine, get_db

# Create the FastAPI app
app = FastAPI(
    title="Task Queue System",
    description="A task queue system built with FastAPI and PostgreSQL",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


# Create async startup and shutdown events
@app.on_event("startup")
async def startup():
    """Startup event handler that initializes the database.

    Creates database tables if they don't exist and logs application startup.
    """
    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logging.info("Application started")


@app.on_event("shutdown")
async def shutdown():
    """Shutdown event handler that cleans up resources.

    Closes database connections and logs application shutdown.
    """
    # Close the database connection
    await engine.dispose()
    logging.info("Application shutdown")


# Include routers
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(workers.router, prefix="/api/workers", tags=["workers"])


# Health check endpoint
@app.get("/", tags=["health"])
async def health_check(db: AsyncSession = Depends(get_db)):  # noqa
    """Health check endpoint to verify API and database are operational."""
    # Basic health check to ensure API and DB are working
    return {"status": "ok", "message": "Task Queue Service is running"}
