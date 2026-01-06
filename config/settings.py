from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from typing import List


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Enterprise Intelligent Search System"
    ENV: str = "local"
    DEBUG: bool = True

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_V1_PREFIX: str = "/api/v1"

    # Database
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "enterprise_search"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    DATABASE_URL: str = (
        "postgresql+psycopg2://postgres:postgres@localhost:5432/enterprise_search"
    )
    # Vector DB
    CHROMA_PERSIST_DIR: str = os.path.abspath("data/chroma")
    CHROMA_COLLECTION: str = "enterprise_documents"

     # Embeddings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384

    # Retrieval
    MAX_RESULTS: int = 5
    SIMILARITY_THRESHOLD: float = 0.2
    
    # ======================
    # CORS
    # ======================
    # CORS_ORIGINS: List[str] = [
    #     "http://localhost:8501",
    #     "http://localhost:3000",
    #     "http://localhost:8000",
    # ]
    CORS_ORIGINS: List[str] = ["*"]
    
    # LLM 
    LLM_PROVIDER: str = "groq"
    LLM_MODEL: str = "llama-3.1-8b-instant"
    GROQ_API_KEY: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
