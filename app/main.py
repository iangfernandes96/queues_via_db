from fastapi import FastAPI, Depends
import logging

from app.api.endpoints import tasks, workers
from app.db.database import engine, get_db, Base
try:
    from sqlalchemy.ext.asyncio import AsyncSession
except ImportError:
    from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from app.core.config import settings

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
    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logging.info("Application started")

@app.on_event("shutdown")
async def shutdown():
    # Close the database connection
    await engine.dispose()
    logging.info("Application shutdown")

# Include routers
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(workers.router, prefix="/api/workers", tags=["workers"])

# Health check endpoint
@app.get("/", tags=["health"])
async def health_check(db: AsyncSession = Depends(get_db)):
    # Basic health check to ensure API and DB are working
    return {"status": "ok", "message": "Task Queue Service is running"} 