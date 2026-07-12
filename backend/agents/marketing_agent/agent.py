"""Nova — FabOPC's Marketing Agent, built on Google ADK."""

from agents._common import build_department_agent
from core.personas import PERSONAS


def build_agent():
    return build_department_agent(
        persona=PERSONAS["marketing"],
        mcp_module="mcp_servers.marketing_servers.mcp_server",
    )


root_agent = build_agent()
