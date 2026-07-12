"""Shared factory for building a FabOPC department agent on Google ADK.

Every agent in agents/*/agent.py is an ADK `LlmAgent` backed by Gemini,
wired to exactly one MCP tool server (its own mcp_servers/<dept>_servers
package) via stdio, following ADK's documented MCPToolset pattern. Each
agent's main.py exposes it as an A2A server with `google.adk.a2a`'s
`to_a2a()` helper, mirroring how InsightForge_temp/agents/*/main.py exposes
a beeai_framework agent as an A2AServer — same "one process per agent"
shape, different underlying framework per the FabOPC proposal's stated
Google ADK + Gemini architecture.
"""

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from mcp import StdioServerParameters

from core.config import get_settings
from core.personas import Persona


def build_department_agent(persona: Persona, mcp_module: str) -> LlmAgent:
    """Build an LlmAgent for one department, tools sourced from its MCP server.

    `mcp_module` is the dotted path to that department's MCP server module
    (e.g. "mcp_servers.finance_servers.mcp_server"), started as a stdio
    subprocess: `python -m <mcp_module>`. Its @mcp.tool()-decorated functions
    are exposed to the agent automatically by MCPToolset.
    """
    settings = get_settings()

    toolset = MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(command="python", args=["-m", mcp_module]),
        )
    )

    return LlmAgent(
        name=persona.name.lower(),
        model=settings.gemini_model,
        description=f"{persona.name}, FabOPC's {persona.role_title}.",
        instruction=persona.system_instruction,
        tools=[toolset],
    )
