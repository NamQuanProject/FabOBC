"""HTTP client for talking to FabOPC's agent A2A servers.

Mirrors the role of InsightForge_temp/app/services/a2a_client.py: the
FastAPI gateway is an A2A *client* to each agent process (see
agents/*/main.py, which serve via google.adk.a2a's to_a2a()). This module
uses the `a2a-sdk` package's A2ACardResolver + A2AClient, which is the
standard client for any A2A-protocol server regardless of the framework
(ADK, beeai_framework, ...) that built it.
"""

import uuid

import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import Message, MessageSendParams, Part, Role, SendMessageRequest, TextPart

from core.agent_registry import agent_url


async def check_agent_online(department: str, timeout_seconds: float = 2.0) -> bool:
    """Fetch an agent's `/.well-known/agent.json` card to check liveness."""
    base_url = agent_url(department)
    try:
        async with httpx.AsyncClient(timeout=timeout_seconds) as http_client:
            resolver = A2ACardResolver(httpx_client=http_client, base_url=base_url)
            await resolver.get_agent_card()
        return True
    except (httpx.HTTPError, httpx.TimeoutException):
        return False


async def send_message_to_agent(
    department: str, message_text: str, timeout_seconds: float = 60.0
) -> str:
    """Send a user message to `department`'s agent and return its reply text.

    `department == "executive"` routes to Orion, the orchestrator, which may
    itself hand off to a department sub-agent (see
    agents/orchestrator_agent/agent.py). Any other key talks directly to
    that department's agent.
    """
    base_url = agent_url(department)

    async with httpx.AsyncClient(timeout=timeout_seconds) as http_client:
        resolver = A2ACardResolver(httpx_client=http_client, base_url=base_url)
        agent_card = await resolver.get_agent_card()

        client = A2AClient(httpx_client=http_client, agent_card=agent_card)

        request = SendMessageRequest(
            id=str(uuid.uuid4()),
            params=MessageSendParams(
                message=Message(
                    role=Role.user,
                    parts=[Part(root=TextPart(text=message_text))],
                    message_id=str(uuid.uuid4()),
                )
            ),
        )

        response = await client.send_message(request)
        return _extract_text(response)


def _extract_text(response) -> str:
    """Pull the first text part out of an A2A SendMessageResponse.

    Structure only — real agent responses may span multiple parts/artifacts
    (e.g. a chart plus a text summary) once tool implementations exist;
    this currently returns the first text part it finds.
    """
    result = getattr(response.root, "result", None)
    if result is None:
        return ""
    parts = getattr(result, "parts", None) or []
    for part in parts:
        text = getattr(getattr(part, "root", None), "text", None)
        if text:
            return text
    return ""
