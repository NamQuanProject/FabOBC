"""MCP tool server for Sage, FabOPC's HR Agent.

Hiring pipeline, job post drafting, headcount, and retention-risk tools.
See mcp_servers/finance_servers/mcp_server.py for the stub convention.
"""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

from mcp_servers.shared.stub import not_implemented

mcp = FastMCP("fabopc-hr")


class HiringPipeline(BaseModel):
    open_roles: int
    candidates_in_pipeline: int
    stalled_candidates: int


class JobPostDraft(BaseModel):
    role_title: str
    body_vi: str
    body_en: str


class HeadcountSummary(BaseModel):
    total_headcount: int
    headcount_by_team: dict[str, int]
    attrition_rate_12m_pct: float
    enps: int


class RetentionRisk(BaseModel):
    employee_ref: str  # anonymized/pseudonymous reference, not raw PII
    department: str
    risk_reason: str
    recommended_action: str


@mcp.tool()
def get_hiring_pipeline(company_id: str) -> HiringPipeline:
    """Summarize open roles and candidate pipeline health.

    Intended source: ATS (applicant tracking system) integration.
    """
    raise not_implemented(
        "get_hiring_pipeline",
        "count open reqs and pipeline candidates by stage from the ATS, "
        "flag candidates stalled >X days at offer stage",
    )


@mcp.tool()
def draft_job_post(company_id: str, role_title: str) -> JobPostDraft:
    """Draft a bilingual job posting for `role_title`.

    Intended source: company profile (industry, size, benefits) from the OPC
    Profile Object plus prior job posts as style reference.
    """
    raise not_implemented(
        "draft_job_post",
        "generate VI/EN job post copy from company profile and role "
        "requirements template",
    )


@mcp.tool()
def get_headcount_summary(company_id: str) -> HeadcountSummary:
    """Report total headcount, per-team breakdown, attrition, and eNPS.

    Intended source: HRIS integration.
    """
    raise not_implemented(
        "get_headcount_summary",
        "aggregate active employee count by team from the HRIS, compute "
        "12-month attrition and latest eNPS survey score",
    )


@mcp.tool()
def get_retention_risks(company_id: str) -> list[RetentionRisk]:
    """Flag employees at elevated attrition risk with a recommended action.

    Intended source: engagement survey signals + tenure/performance data,
    cross-referenced with Operations' workload signals in the OPC Profile
    Object (Gallup-style link between workload and disengagement, per the
    proposal's problem statement).
    """
    raise not_implemented(
        "get_retention_risks",
        "combine survey sentiment, review overdue flags, and workload "
        "signals shared by Operations to rank retention risk",
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
