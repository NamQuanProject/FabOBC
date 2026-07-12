"""MCP tool server for Atlas, FabOPC's Finance Agent.

Exposes read/analysis tools over the company's accounting and banking data.
Started standalone (`python -m mcp_servers.finance_servers.mcp_server`) and
connected to by agents/finance_agent/agent.py via an MCPToolset over stdio.

All tool bodies are intentionally unimplemented stubs — see
mcp_servers/shared/stub.py. Wiring these up means replacing each
`raise not_implemented(...)` with a real query against the company's
accounting integration / opc_profiles data.
"""

from datetime import date

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

from mcp_servers.shared.stub import not_implemented

mcp = FastMCP("fabopc-finance")


class CashPosition(BaseModel):
    company_id: str
    cash_balance_vnd: float
    monthly_burn_vnd: float
    runway_months: float
    inflow_vnd_last_30d: float


class MarginScenario(BaseModel):
    label: str  # "best" | "base" | "downside"
    projected_margin_pct: float
    assumptions: list[str]


class ReceivableItem(BaseModel):
    customer_name: str
    amount_vnd: float
    days_overdue: int


class BudgetSummary(BaseModel):
    period: str
    revenue_vnd: float
    opex_vnd: float
    largest_variance_category: str
    variance_pct: float


@mcp.tool()
def get_cash_position(company_id: str) -> CashPosition:
    """Return current cash balance, burn rate, and runway in months.

    Intended source: the company's accounting/banking integration, cached
    into department_kpis / the OPC Profile Object's finance department
    context. Backs the Finance dashboard's cash KPIs and the "What's our
    cash position?" chat prompt.
    """
    raise not_implemented(
        "get_cash_position",
        "aggregate operating + reserve account balances and 30d inflow to "
        "compute runway_months = cash_balance_vnd / monthly_burn_vnd",
    )


@mcp.tool()
def model_margin_scenarios(company_id: str, quarter: str) -> list[MarginScenario]:
    """Produce best/base/downside net-margin scenarios for the given quarter.

    Intended source: current margin trend from accounting data plus
    operations-agent cost signals (e.g. logistics cost changes) read from the
    shared OPC Profile Object.
    """
    raise not_implemented(
        "model_margin_scenarios",
        "project net margin under 3 scenarios by combining historical margin "
        "trend with cost/revenue signals shared by other department agents",
    )


@mcp.tool()
def list_overdue_receivables(company_id: str) -> list[ReceivableItem]:
    """List customers with overdue accounts receivable, most overdue first.

    Intended source: AR aging report from the accounting integration.
    """
    raise not_implemented(
        "list_overdue_receivables",
        "query AR aging table, filter days_overdue > 0, sort descending",
    )


@mcp.tool()
def get_budget_summary(company_id: str, period: str) -> BudgetSummary:
    """Summarize month-to-date revenue vs. OPEX against budget for `period`.

    Intended source: accounting integration budget vs. actuals report.
    """
    raise not_implemented(
        "get_budget_summary",
        "compare actuals to budget per line item, surface the category with "
        "the largest variance_pct",
    )


@mcp.tool()
def get_next_filing_impact(company_id: str, as_of: date) -> str:
    """Explain how upcoming compliance obligations affect cash flow.

    Cross-agent tool: reads compliance_obligations written by Lex (Compliance
    Agent) via the OPC Profile Object so Finance can factor tax due-dates
    into cash planning.
    """
    raise not_implemented(
        "get_next_filing_impact",
        "read compliance obligations from the OPC Profile Object due within "
        "30 days of as_of and net them against get_cash_position()",
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
