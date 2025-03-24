import asyncio
from datetime import datetime, timedelta

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.db.models import Task, TaskStatus
from app.schemas.task import TaskCreate
from app.services.task_queue import TaskQueueService


@pytest_asyncio.fixture
async def db_session():
    # Create an in-memory SQLite database for testing
    # Using SQLite for simplicity, although it has limited async support
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    TestingSessionLocal = sessionmaker(
        class_=AsyncSession, expire_on_commit=False, bind=engine
    )

    async with TestingSessionLocal() as session:
        yield session
        # Clean up
        await session.close()

    await engine.dispose()


@pytest.mark.asyncio
async def test_create_task(db_session):
    # Create a task
    task_in = TaskCreate(
        name="test_task", payload={"key": "value"}, priority=2, scheduled_at=None
    )

    task = await TaskQueueService.create_task(db=db_session, task_in=task_in)

    # Test that the task was created correctly
    assert task.id is not None
    assert task.name == "test_task"
    assert task.payload == {"key": "value"}
    assert task.priority == 2
    assert task.status == TaskStatus.PENDING
    assert task.scheduled_at is None


@pytest.mark.asyncio
async def test_scheduled_task(db_session):
    # Create a scheduled task
    future_time = datetime.utcnow() + timedelta(hours=1)
    task_in = TaskCreate(
        name="scheduled_task",
        payload={"key": "value"},
        priority=2,
        scheduled_at=future_time,
    )

    task = await TaskQueueService.create_task(db=db_session, task_in=task_in)

    # Test that the task was created with the correct scheduled status
    assert task.status == TaskStatus.SCHEDULED
    assert task.scheduled_at == future_time


@pytest.mark.asyncio
async def test_get_task(db_session):
    # Create a task
    task_in = TaskCreate(
        name="get_task", payload={"key": "value"}, priority=2, scheduled_at=None
    )
    created_task = await TaskQueueService.create_task(db=db_session, task_in=task_in)

    # Get the task
    task = await TaskQueueService.get_task(db=db_session, task_id=created_task.id)

    # Test that we got the correct task
    assert task is not None
    assert task.id == created_task.id
    assert task.name == "get_task"


@pytest.mark.asyncio
async def test_pause_and_resume_task(db_session):
    # Create a task
    task_in = TaskCreate(
        name="pause_resume_task",
        payload={"key": "value"},
        priority=2,
        scheduled_at=None,
    )
    created_task = await TaskQueueService.create_task(db=db_session, task_in=task_in)

    # Pause the task
    paused_task = await TaskQueueService.pause_task(
        db=db_session, task_id=created_task.id
    )
    assert paused_task.status == TaskStatus.PAUSED

    # Resume the task
    resumed_task = await TaskQueueService.resume_task(
        db=db_session, task_id=created_task.id
    )
    assert resumed_task.status == TaskStatus.PENDING
