from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:pass@db:5432/hiring"
    REDIS_URL: str = "redis://redis:6379/0"
    GREENHOUSE_API_KEY: str = ""
    GREENHOUSE_BASE_URL: str = "https://harvest.greenhouse.io/v1"
    LEVER_API_KEY: str = ""
    LEVER_BASE_URL: str = "https://api.lever.co/v1"
    MODEL_PATH: str = "app/ml/model.pkl"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
