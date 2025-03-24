import os
from pydantic import PostgresDsn, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Queue System"
    API_V1_STR: str = "/api"
    
    DATABASE_URL: PostgresDsn = Field(
        default="postgresql://postgres:postgres@postgres:5432/taskqueue"
    )
    
    # Worker settings
    WORKER_POLL_INTERVAL: int = int(os.getenv("WORKER_POLL_INTERVAL", "5"))
    WORKER_MAX_TASKS: int = int(os.getenv("WORKER_MAX_TASKS", "10"))
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings() 