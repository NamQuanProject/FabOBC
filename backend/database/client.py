"""The backend's only data access path: Supabase's REST API (PostgREST).

FabOPC has no self-hosted database and the backend never opens a direct
Postgres/asyncpg connection — every read/write goes through this async
Supabase client over HTTPS, the same way InsightForge_temp used the
Supabase client for storage/auth. Tables are created and seeded directly in
the Supabase SQL Editor (see sql/init_postgresql.sql, sql/seed_sample_data.sql)
— the backend never runs DDL and doesn't need network access to Postgres's
own port.

SUPABASE_KEY should be the project's **service_role** secret for the
backend (Project Settings -> API), not the anon/publishable key the
frontend would use — the backend is a trusted context and needs to read/
write freely regardless of any Row Level Security policies you add later.
"""

from supabase import AsyncClient, acreate_client

from core.config import get_settings

_client: AsyncClient | None = None


async def get_async_supabase_client() -> AsyncClient:
    """Lazily create and cache the process-wide async Supabase client."""
    global _client
    if _client is None:
        settings = get_settings()
        if not settings.supabase_url or not settings.supabase_key:
            raise RuntimeError(
                "SUPABASE_URL and SUPABASE_KEY must be set to reach the database."
            )
        _client = await acreate_client(settings.supabase_url, settings.supabase_key)
    return _client
