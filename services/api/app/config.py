from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = "taxi-lakehouse-ai-agent"
    openai_api_key: str = "replace-me"
    openai_model: str = "gpt-4.1-mini"
    duckdb_path: str = "/data/warehouse/analytics.duckdb"
    semantic_catalog_path: str = "/app/contracts/semantic_catalog.yaml"
    query_audit_log_path: str = "/data/warehouse/query_audit.jsonl"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def semantic_catalog(self) -> Path:
        return Path(self.semantic_catalog_path)


@lru_cache
def get_settings() -> Settings:
    return Settings()
