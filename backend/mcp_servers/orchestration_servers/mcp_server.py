"""MCP tool server for Orion, FabOPC's Orchestrator Agent.

Tools for reading/writing the shared OPC Profile Object (Innovation 1),
checking department agent liveness, and composing cross-department
summaries. Department agents call `update_opc_profile` to publish findings
that other agents should see; Orion calls the read tools to compose
briefings. See mcp_servers/finance_servers/mcp_server.py for the stub
convention.
"""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

from mcp_servers.shared.stub import not_implemented

mcp = FastMCP("fabopc-orchestration")


class AgentStatus(BaseModel):
    department: str
    persona_name: str
    online: bool
    last_response_at: str | None = None


class ApprovalItem(BaseModel):
    department: str
    description: str
    exposure_vnd: float | None = None


class ExecutiveBriefing(BaseModel):
    headline: str
    department_summaries: dict[str, str]
    pending_approvals: list[ApprovalItem]


@mcp.tool()
def get_agent_status(company_id: str) -> list[AgentStatus]:
    """Report liveness of every department agent's A2A server.

    Intended source: A2A agent-card health check against each agent URL in
    core.agent_registry.AGENTS (mirrors app/services/a2a_client.py).
    """
    raise not_implemented(
        "get_agent_status",
        "ping each agent's A2A server (GET /.well-known/agent.json) and "
        "report reachability plus last successful task timestamp",
    )


@mcp.tool()
def get_opc_profile(company_id: str) -> dict:
    """Fetch the current OPC Profile Object for `company_id` as a dict.

    Intended source: opc_profiles.profile JSONB column, deserialized via
    core.opc_profile.OPCProfileObject.
    """
    raise not_implemented(
        "get_opc_profile",
        "load opc_profiles row for company_id and return the profile JSONB",
    )


@mcp.tool()
def update_opc_profile(company_id: str, department: str, patch: dict) -> dict:
    """Merge `patch` into the department's slice of the shared OPC Profile Object.

    Called by department agents (e.g. Finance writing a 'cash_flow_tightening'
    signal) so downstream agents (Operations, Compliance, BI) see it without
    re-querying the source system. See
    core.opc_profile.OPCProfileObject.upsert_department_signal.
    """
    raise not_implemented(
        "update_opc_profile",
        "load the OPC Profile Object, apply patch to departments[department], "
        "persist back to opc_profiles.profile",
    )


@mcp.tool()
def get_pending_approvals(company_id: str) -> list[ApprovalItem]:
    """List items across all departments awaiting the CEO's approval.

    Intended source: department_tasks rows with status in a
    manager-approval-required state, aggregated across departments.
    """
    raise not_implemented(
        "get_pending_approvals",
        "query department_tasks across all departments for approval-pending "
        "statuses and sum any associated exposure_vnd",
    )


@mcp.tool()
def compose_executive_briefing(company_id: str) -> ExecutiveBriefing:
    """Compose a cross-department morning briefing from the OPC Profile Object.

    Intended source: get_opc_profile() department signals + get_pending_approvals(),
    summarized per department.
    """
    raise not_implemented(
        "compose_executive_briefing",
        "pull each department's active_signals from the OPC Profile Object "
        "and pending_approvals, and summarize into one headline + per-dept "
        "summary",
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
