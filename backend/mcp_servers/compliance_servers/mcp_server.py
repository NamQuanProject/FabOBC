"""MCP tool server for Lex, FabOPC's Compliance Agent.

Implements the "Context-Aware Compliance and Policy Coordination" pipeline
from the FabOPC proposal (Innovation 2): use the OPC Profile Object + company
knowledge base to identify obligations, compute payable amounts, and surface
recoverable deductions — always as structured action items, not legal advice.
See mcp_servers/finance_servers/mcp_server.py for the stub convention.
"""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

from mcp_servers.shared.stub import not_implemented

mcp = FastMCP("fabopc-compliance")


class FilingObligation(BaseModel):
    obligation_code: str  # e.g. "01/GTGT" (VAT), "PIT", "CIT"
    description: str
    due_date: str
    amount_vnd: float | None = None
    status: str  # "action_needed" | "draft_ready" | "scheduled" | "filed"


class VatCalculation(BaseModel):
    period: str
    output_vat_vnd: float
    recorded_input_vat_vnd: float
    payable_vnd: float
    unrecorded_recoverable_input_vat_vnd: float


class DeductionItem(BaseModel):
    description: str
    amount_vnd: float
    source_reference: str


class ComplianceStatus(BaseModel):
    score_out_of_100: int
    filings_ytd: int
    on_time_pct: float
    open_audit_flags: int


@mcp.tool()
def get_upcoming_filings(company_id: str) -> list[FilingObligation]:
    """List upcoming tax/regulatory filings relevant to this company.

    Intended source: obligation rules matched against the company's OPC
    Profile Object (business type, industry, operating location) — this is
    the "context-aware" matching described in the proposal's Innovation 2,
    not a generic legal database dump.
    """
    raise not_implemented(
        "get_upcoming_filings",
        "match statutory obligation rules (VAT/PIT/CIT/social insurance/"
        "e-invoicing) against the company's OPC Profile Object attributes",
    )


@mcp.tool()
def calculate_vat_payable(company_id: str, period: str) -> VatCalculation:
    """Compute VAT payable for `period`, flagging unrecorded recoverable input VAT.

    Intended source: accounting integration invoice/output-tax records,
    cross-checked against uploaded supplier invoices not yet recorded.
    """
    raise not_implemented(
        "calculate_vat_payable",
        "payable_vnd = output_vat_vnd - recorded_input_vat_vnd; separately "
        "surface unrecorded supplier invoices as recoverable input VAT",
    )


@mcp.tool()
def find_recoverable_deductions(company_id: str) -> list[DeductionItem]:
    """Find recoverable input VAT / miscoded deductible expenses.

    Intended source: supplier invoices and expense records not yet reflected
    in the accounting system's recorded input VAT.
    """
    raise not_implemented(
        "find_recoverable_deductions",
        "scan uploaded supplier invoices and expense entries for items not "
        "yet recorded or miscoded as non-deductible",
    )


@mcp.tool()
def get_compliance_status(company_id: str) -> ComplianceStatus:
    """Report an overall compliance health score and filing track record.

    Intended source: compliance_obligations history (filed vs. due on time).
    """
    raise not_implemented(
        "get_compliance_status",
        "score = weighted function of on-time filing rate and open audit "
        "flags over the trailing 12 months",
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
