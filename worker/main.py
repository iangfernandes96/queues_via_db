import asyncio
import logging
import os
import signal
import socket
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings
from app.services.task_queue import TaskQueueService
from app.services.worker import WorkerService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("worker")

# Create database connection
# Convert PostgreSQL URL to AsyncPG format
SQLALCHEMY_DATABASE_URL = str(settings.DATABASE_URL).replace(
    "postgresql://", "postgresql+asyncpg://"
)
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


@asynccontextmanager
async def get_db():
    """Get a database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


class Worker:
    def __init__(self):
        self.running = True
        self.worker_id: Optional[UUID] = None
        self.worker_name = f"worker-{socket.gethostname()}-{os.getpid()}"
        self.poll_interval = settings.WORKER_POLL_INTERVAL
        self.max_tasks = settings.WORKER_MAX_TASKS

        # Set up signal handlers
        signal.signal(signal.SIGTERM, self.handle_signal)
        signal.signal(signal.SIGINT, self.handle_signal)

        logger.info(f"Worker {self.worker_name} starting up")

    def handle_signal(self, signum, frame):
        """Handle termination signals."""
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False

    async def register_worker(self):
        """Register worker in the database."""
        async with get_db() as db:
            worker = await WorkerService.create_worker(db=db, name=self.worker_name)
            self.worker_id = worker.id
            logger.info(f"Worker registered with ID: {self.worker_id}")

    async def update_heartbeat(self):
        """Update the worker's heartbeat in the database."""
        if self.worker_id is None:
            logger.error("Worker ID is None, cannot update heartbeat")
            return None

        async with get_db() as db:
            await WorkerService.update_heartbeat(db=db, worker_id=self.worker_id)

    async def process_task(self, task):
        """Process a task."""
        logger.info(f"Processing task {task.id}: {task.name}")

        try:
            # Here you would implement the actual task execution
            # This is a simple example that just sleeps for a few seconds
            result = {
                "status": "success",
                "processed_at": datetime.utcnow().isoformat(),
            }

            # In a real implementation, you would process the task payload
            # and return a result based on the processing

            # Sleep to simulate processing time - use asyncio.sleep for async operation
            await asyncio.sleep(2)

            # Mark the task as completed
            async with get_db() as db:
                await TaskQueueService.complete_task(
                    db=db, task_id=task.id, result=result
                )
                logger.info(f"Task {task.id} completed successfully")

            return True
        except Exception as e:
            # If an error occurs, mark the task as failed
            error_message = str(e)
            logger.error(f"Error processing task {task.id}: {error_message}")

            async with get_db() as db:
                await TaskQueueService.fail_task(
                    db=db, task_id=task.id, error=error_message
                )

            return False

    async def run(self):
        """Run the worker loop."""
        await self.register_worker()
        logger.info(f"Worker {self.worker_id} ({self.worker_name}) started")

        last_heartbeat_time = datetime.utcnow()
        heartbeat_interval = 30  # seconds

        try:
            while self.running:
                # Update heartbeat every 30 seconds
                current_time = datetime.utcnow()
                if (
                    current_time - last_heartbeat_time
                ).total_seconds() >= heartbeat_interval:
                    await self.update_heartbeat()
                    last_heartbeat_time = current_time

                # Get next task
                if self.worker_id is None:
                    logger.error("Worker ID is None, cannot get next task")
                    await asyncio.sleep(5)  # Wait before retrying
                    continue

                async with get_db() as db:
                    task = await TaskQueueService.get_next_task(
                        db=db, worker_id=self.worker_id
                    )

                if task:
                    # Process the task
                    await self.process_task(task)
                else:
                    # No tasks available, sleep for poll_interval seconds
                    logger.debug(
                        f"No tasks available, sleeping for {self.poll_interval} seconds"
                    )
                    # Use asyncio.sleep for async operation
                    for _ in range(self.poll_interval):
                        if not self.running:
                            break
                        await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Worker error: {str(e)}")
        finally:
            # Mark worker as inactive when shutting down
            if self.worker_id is not None:
                async with get_db() as db:
                    await WorkerService.set_worker_status(
                        db=db, worker_id=self.worker_id, status="inactive"
                    )
                logger.info(f"Worker {self.worker_id} ({self.worker_name}) shut down")
            else:
                logger.info(f"Worker ({self.worker_name}) shut down (no ID registered)")


async def main():
    worker = Worker()
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
