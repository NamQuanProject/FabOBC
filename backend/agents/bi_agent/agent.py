"""Echo — FabOPC's Business Intelligence Agent, built on Google ADK."""

from agents._common import build_department_agent
from core.personas import PERSONAS


def build_agent():
    return build_department_agent(
        persona=PERSONAS["bi"],
        mcp_module="mcp_servers.bi_servers.mcp_server",
    )


root_agent = build_agent()
