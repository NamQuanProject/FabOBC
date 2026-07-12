from fastapi import APIRouter

from app.schema.agents import AgentStatusOut
from app.services.a2a_client import check_agent_online
from core.agent_registry import AGENTS, agent_url

router = APIRouter(prefix="/api/v1/agents", tags=["agents"])


@router.get("/status", response_model=list[AgentStatusOut])
async def get_agents_status() -> list[AgentStatusOut]:
    """Liveness of every agent's A2A server, for the frontend's 'online' badges.

    Requires each agent process (agents/*/main.py) to actually be running;
    returns online=False rather than erroring if one is unreachable.
    """
    statuses = []
    for key, descriptor in AGENTS.items():
        online = await check_agent_online(key)
        statuses.append(
            AgentStatusOut(
                department=key,
                persona_name=descriptor.persona_name,
                role_title=descriptor.role_title,
                online=online,
                url=agent_url(key),
            )
        )
    return statuses
