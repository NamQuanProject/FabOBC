"""Static registry describing every agent in the FabOPC executive team.

This mirrors InsightForge_temp/agents/config.py's role but covers FabOPC's
seven agents (one orchestrator + six department agents). The FastAPI gateway
uses this to build A2A client URLs and to report `/api/v1/agents/status`;
each agent's own `main.py` uses its entry to know which port to bind.
"""

from dataclasses import dataclass

from core.config import get_settings


@dataclass(frozen=True)
class AgentDescriptor:
    key: str  # matches Department key used across DB + frontend
    persona_name: str  # e.g. "Atlas"
    role_title: str  # e.g. "Finance Agent"
    port_attr: str  # attribute name on Settings holding this agent's port
    mcp_module: str  # dotted path to this agent's MCP server module


AGENTS: dict[str, AgentDescriptor] = {
    "executive": AgentDescriptor(
        key="executive",
        persona_name="Orion",
        role_title="Virtual CEO / Orchestrator",
        port_attr="orchestrator_agent_port",
        mcp_module="mcp_servers.orchestration_servers.mcp_server",
    ),
    "finance": AgentDescriptor(
        key="finance",
        persona_name="Atlas",
        role_title="Finance Agent",
        port_attr="finance_agent_port",
        mcp_module="mcp_servers.finance_servers.mcp_server",
    ),
    "marketing": AgentDescriptor(
        key="marketing",
        persona_name="Nova",
        role_title="Marketing Agent",
        port_attr="marketing_agent_port",
        mcp_module="mcp_servers.marketing_servers.mcp_server",
    ),
    "operations": AgentDescriptor(
        key="operations",
        persona_name="Forge",
        role_title="Operations Agent",
        port_attr="operations_agent_port",
        mcp_module="mcp_servers.operations_servers.mcp_server",
    ),
    "hr": AgentDescriptor(
        key="hr",
        persona_name="Sage",
        role_title="HR Agent",
        port_attr="hr_agent_port",
        mcp_module="mcp_servers.hr_servers.mcp_server",
    ),
    "compliance": AgentDescriptor(
        key="compliance",
        persona_name="Lex",
        role_title="Compliance Agent",
        port_attr="compliance_agent_port",
        mcp_module="mcp_servers.compliance_servers.mcp_server",
    ),
    "bi": AgentDescriptor(
        key="bi",
        persona_name="Echo",
        role_title="Business Intelligence Agent",
        port_attr="bi_agent_port",
        mcp_module="mcp_servers.bi_servers.mcp_server",
    ),
}


def agent_url(key: str) -> str:
    """Base URL of an agent's A2A server, e.g. http://127.0.0.1:9991"""
    settings = get_settings()
    descriptor = AGENTS[key]
    port = getattr(settings, descriptor.port_attr)
    return f"http://{settings.agent_host}:{port}"
