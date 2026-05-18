"""
Application configuration settings.
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Application settings
    PROJECT_NAME: str = "AI Astrology Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000"],  # Next.js default port
        description="List of origins that are allowed to make cross-origin requests"
    )

    # Database settings
    DATABASE_URL: str = Field(
        default="postgresql://user:password@localhost:5432/astrology_db",
        description="PostgreSQL database connection URL"
    )

    # Redis settings (for caching and Celery)
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL"
    )

    # Celery settings
    CELERY_BROKER_URL: str = Field(
        default="redis://localhost:6379/1",
        description="Celery broker URL"
    )
    CELERY_RESULT_BACKEND: str = Field(
        default="redis://localhost:6379/2",
        description="Celery result backend URL"
    )

    # AI service settings
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None

    # Security settings
    SECRET_KEY: str = Field(
        default="your-secret-key-here-change-in-production",
        description="Secret key for JWT token generation"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"

    # File upload settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_FOLDER: str = "./uploads"

    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    model_config = {
        "case_sensitive": True,
        "env_file": ".env"
    }

settings = Settings()