"""The OPC Profile Object (OPO) — FabOPC's Innovation 1.

A structured, Pydantic-validated shared state layer initialized by the
Orchestrator Agent during onboarding. Every department agent reads from and
writes to the same OPO instance for a company, so a finding made by one
agent (e.g. Finance flags tightening cash flow) is immediately visible to
every other agent (Operations, Compliance, BI, ...) without re-entering data.

Persistence: the OPO is stored as JSONB on `opc_profiles.profile` (see
app/models.py) and hydrated into this model at read time. Agents mutate a
copy and the service layer persists the diff back — see
app/services/opc_profile_service.py (structure only, not yet implemented).
"""

from datetime import datetime

from pydantic import BaseModel, Field


class CompanyIdentity(BaseModel):
    company_id: str
    legal_name: str
    industry: str | None = None
    founded_year: int | None = None
    headquarters: str | None = None
    tax_id: str | None = None
    employee_count: int | None = None
    annual_revenue_vnd: float | None = None
    digital_maturity_level: int | None = Field(
        default=None, ge=1, le=5, description="Decision 1567 digital maturity, 1-5"
    )


class DepartmentContext(BaseModel):
    """Per-department slice of shared state, written by that department's agent."""

    department: str
    agent_persona: str
    last_synced_at: datetime | None = None
    active_signals: list[str] = Field(
        default_factory=list,
        description="Short machine-readable findings other agents can react to, "
        "e.g. 'cash_flow_tightening', 'supplier_delay:3_orders'.",
    )
    notes: dict[str, str] = Field(default_factory=dict)


class ComplianceObligation(BaseModel):
    obligation_code: str
    description: str
    due_date: datetime | None = None
    responsible_department: str | None = None
    risk_level: str | None = None
    status: str = "pending"


class KnowledgeSourceRef(BaseModel):
    source_id: str
    title: str
    source_type: str  # doc | spreadsheet | accounting | crm | other
    indexed: bool = False


class OPCProfileObject(BaseModel):
    """The full shared operational context for one company workspace."""

    identity: CompanyIdentity
    departments: dict[str, DepartmentContext] = Field(default_factory=dict)
    obligations: list[ComplianceObligation] = Field(default_factory=list)
    knowledge_sources: list[KnowledgeSourceRef] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def upsert_department_signal(self, department: str, signal: str) -> None:
        """Append a cross-agent-visible signal; called by department agents.

        Structure only — real invocation happens via the orchestration MCP
        server's `update_opc_profile` tool (mcp_servers/orchestration_servers),
        which is not yet implemented.
        """
        ctx = self.departments.setdefault(
            department,
            DepartmentContext(department=department, agent_persona=""),
        )
        if signal not in ctx.active_signals:
            ctx.active_signals.append(signal)
        self.updated_at = datetime.utcnow()
