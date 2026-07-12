"""Orion — FabOPC's Orchestrator Agent (virtual CEO), built on Google ADK.

Unlike the department agents (agents/_common.py), Orion does not primarily
call domain tools directly — it routes to the six department agents as
remote A2A sub-agents and synthesizes their responses, using its own
orchestration MCP tools (get_opc_profile, get_pending_approvals, etc.) to
ground cross-department summaries. This mirrors InsightForge_temp's
RoutingAgent (agents/orchestration_agent/agent.py), which hands off between
its TrendingAnalysisAgent and ContentGeneratingAgent — here generalized to
six department agents instead of two.
"""

from google.adk.agents import LlmAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from mcp import StdioServerParameters

from core.agent_registry import AGENTS, agent_url
from core.config import get_settings
from core.personas import PERSONAS

_DEPARTMENT_KEYS = ["finance", "marketing", "operations", "hr", "compliance", "bi"]


def _build_department_sub_agents() -> list[RemoteA2aAgent]:
    """One RemoteA2aAgent per department, pointed at that agent's A2A server.

    Each department agent is started as its own process (see
    agents/finance_agent/main.py and siblings) before the orchestrator can
    successfully hand off to it.
    """
    sub_agents = []
    for key in _DEPARTMENT_KEYS:
        descriptor = AGENTS[key]
        sub_agents.append(
            RemoteA2aAgent(
                name=descriptor.persona_name.lower(),
                description=f"{descriptor.persona_name}, FabOPC's {descriptor.role_title}.",
                agent_card=f"{agent_url(key)}/.well-known/agent.json",
            )
        )
    return sub_agents


def build_agent() -> LlmAgent:
    settings = get_settings()
    persona = PERSONAS["executive"]

    orchestration_toolset = MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="python",
                args=["-m", "mcp_servers.orchestration_servers.mcp_server"],
            ),
        )
    )

    return LlmAgent(
        name=persona.name.lower(),
        model=settings.gemini_model,
        description=f"{persona.name}, FabOPC's {persona.role_title}.",
        instruction=persona.system_instruction,
        tools=[orchestration_toolset],
        sub_agents=_build_department_sub_agents(),
    )


root_agent = build_agent()
