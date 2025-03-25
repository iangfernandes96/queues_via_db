"""Configuration settings for the Task Queue System.

This module defines the application settings using Pydantic for validation.
"""
import os
from typing import Any, Optional

from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings.

    Loads configuration from environment variables with defaults.
    """

    PROJECT_NAME: str = "Task Queue System"
    API_V1_STR: str = "/api"

    # Database connection
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: str = "5432"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "taskqueue"
    DATABASE_URL: Optional[PostgresDsn] = None

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info) -> Any:
        """Assemble database connection URL.

        Construct from components or use the provided value.
        """
        if isinstance(v, str):
            return v
        values = info.data
        db_name = values.get("POSTGRES_DB", "")
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{db_name}",
        )

    # Worker settings
    WORKER_POLL_INTERVAL: int = int(os.getenv("WORKER_POLL_INTERVAL", "5"))
    WORKER_MAX_TASKS: int = int(os.getenv("WORKER_MAX_TASKS", "10"))

    class Config:
        """Pydantic configuration class."""

        env_file = ".env"
        case_sensitive = True


settings = Settings()
