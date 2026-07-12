from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.agents import router as agents_router
from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.departments import router as departments_router
from app.api.health import router as health_router
from app.api.opc_profile import router as opc_profile_router
from app.api.users import router as users_router
from app.db import init_db
from core.config import get_settings

app = FastAPI(
    title="FabOPC API",
    description=(
        "Gateway for FabOPC's private multi-agent AI management layer. "
        "Talks to the Orchestrator + department agents over A2A "
        "(see app/services/a2a_client.py) and persists shared state in "
        "Postgres/Supabase (see app/db.py, core/opc_profile.py)."
    ),
    version="0.1.0",
)

settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()


app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(departments_router)
app.include_router(opc_profile_router)
app.include_router(agents_router)
app.include_router(chat_router)
