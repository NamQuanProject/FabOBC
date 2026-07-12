"""Central runtime configuration for the FabOPC backend.

All agent servers, MCP servers, and the FastAPI gateway read settings from
here so port numbers, model names, and credentials stay consistent across
processes that are started independently (see agents/*/main.py).
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- Supabase ---------------------------------------------------------
    # No self-hosted database, no direct Postgres connection: the backend
    # reaches Supabase over its REST API (see database/client.py).
    # SUPABASE_KEY should be the service_role secret for backend use.
    supabase_url: str | None = None
    supabase_key: str | None = None

    # --- Gemini / Google ADK --------------------------------------------------
    google_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"

    # --- FastAPI gateway --------------------------------------------------
    cors_allow_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    # --- Agent host/ports (A2A servers, one process per agent) --------------
    agent_host: str = "127.0.0.1"
    orchestrator_agent_port: int = 9990
    finance_agent_port: int = 9991
    marketing_agent_port: int = 9992
    operations_agent_port: int = 9993
    hr_agent_port: int = 9994
    compliance_agent_port: int = 9995
    bi_agent_port: int = 9996

    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.cors_allow_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
