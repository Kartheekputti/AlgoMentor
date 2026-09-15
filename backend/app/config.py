from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AlgoMentor"
    app_env: str = "development"
    app_port: int = 8000
    secret_key: str = "dev-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "algomentor"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"

    redis_host: str = "localhost"
    redis_port: int = 6379

    qdrant_host: str = "localhost"
    qdrant_port: int = 6333

    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    embedding_model: str = "mxbai-embed-large"
    embedding_dimension: int = 1024
    qdrant_collection: str = "algomentor_dsa_knowledge_mxbai"
    retrieval_k: int = 4
    debug_rag: bool = True

    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins_list(self):
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
