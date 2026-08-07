from typing import List, Optional
# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "PromptShield AI"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "promptshield_super_secret_jwt_key_32bytes_min_length_spec!"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database & Redis (Defaults to sqlite & in-memory/mock fallback for easy local dev & testing)
    DATABASE_URL: str = "sqlite+aiosqlite:///./promptshield.db"
    REDIS_URL: str = "redis://localhost:6379/0"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Optional LLM API Key for Semantic Classifier Deep Mode
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
