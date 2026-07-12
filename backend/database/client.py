"""Supabase client helper, mirrored from InsightForge_temp/database/client.py.

Used for anything better served by the Supabase SDK than raw SQL (storage
buckets for uploaded knowledge sources, auth admin calls, realtime channels).
Structured relational access (users, OPC profiles, KPIs, tasks) goes through
SQLAlchemy in app/db.py instead.
"""

from functools import lru_cache

from supabase import Client, create_client

from core.config import get_settings


@lru_cache
def get_supabase_client() -> Client:
    settings = get_settings()
    if not settings.supabase_url or not settings.supabase_key:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_KEY must be set to use the Supabase client."
        )
    return create_client(settings.supabase_url, settings.supabase_key)
