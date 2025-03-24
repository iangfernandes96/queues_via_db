from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Convert PostgreSQL URL to AsyncPG format
# Replace postgresql:// with postgresql+asyncpg://
SQLALCHEMY_DATABASE_URL = str(settings.DATABASE_URL).replace(
    "postgresql://", "postgresql+asyncpg://"
)

# Create async engine
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_db():
    """Dependency for getting async DB session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
