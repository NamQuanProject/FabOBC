"""Shared FastAPI dependencies."""

from supabase import AsyncClient

from database.client import get_async_supabase_client


async def get_supabase() -> AsyncClient:
    return await get_async_supabase_client()
