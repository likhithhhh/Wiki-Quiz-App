from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables.

    Environment variables:
    - GEMINI_API_KEY
    - DATABASE_URL (e.g. postgresql+psycopg2://user:pass@localhost:5432/wiki_quiz)
    - FRONTEND_ORIGIN (optional, defaults to http://localhost:5173)
    """

    GEMINI_API_KEY: str
    GROQ_API_KEY: str | None = None
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/wiki_quiz"
    APP_NAME: str = "Wiki Quiz App"
    FRONTEND_ORIGIN: str = "http://localhost:5173"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()


