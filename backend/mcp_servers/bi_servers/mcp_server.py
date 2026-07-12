"""MCP tool server for Echo, FabOPC's Business Intelligence Agent.

Implements the three-stage "Internal Data Intelligence" pipeline from the
FabOPC proposal (Innovation 3):
  Stage 1 — ingest_business_data: load/validate/normalize an uploaded CSV or
            Excel file into a standardized internal schema.
  Stage 2 — detect_trends_and_anomalies: analyze the normalized dataset for
            revenue trends, cost pressure, customer concentration, anomalies.
  Stage 3 — generate_prioritized_recommendations: convert detected patterns
            into at most three prioritized, plain-language recommendations.
Plus forecast_revenue and get_churn_risk_accounts as supporting tools.
See mcp_servers/finance_servers/mcp_server.py for the stub convention.
"""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

from mcp_servers.shared.stub import not_implemented

mcp = FastMCP("fabopc-bi")


class IngestionResult(BaseModel):
    rows_ingested: int
    rows_rejected: int
    detected_schema: dict[str, str]  # column -> inferred type
    normalization_notes: list[str]


class DetectedSignal(BaseModel):
    dimension: str  # "revenue_trend" | "cost_pressure" | "customer_concentration" | "anomaly"
    description: str
    magnitude_pct: float | None = None
    supporting_observation: str


class Recommendation(BaseModel):
    action: str
    reason: str
    supporting_data_reference: str


class RevenueForecast(BaseModel):
    horizon_quarters: int
    point_estimate_vnd: float
    confidence_low_vnd: float
    confidence_high_vnd: float
    historical_accuracy_pct: float


class ChurnRiskAccount(BaseModel):
    account_name: str
    annual_value_vnd: float
    churn_probability_pct: float
    signal: str


@mcp.tool()
def ingest_business_data(company_id: str, file_ref: str) -> IngestionResult:
    """Stage 1: load and normalize an uploaded CSV/Excel file of business records.

    Handles inconsistent date formats, currency notation, missing values,
    duplicate entries, and irregular spreadsheet structures. Normalized
    output is intended to be written into the OPC Profile Object and
    semantic memory so other agents can reuse it without re-entering data.
    """
    raise not_implemented(
        "ingest_business_data",
        "parse file_ref, infer column types, normalize dates/currency, "
        "dedupe rows, and write the cleaned dataset reference into the OPC "
        "Profile Object",
    )


@mcp.tool()
def detect_trends_and_anomalies(company_id: str) -> list[DetectedSignal]:
    """Stage 2: analyze the normalized dataset for trends, risk, and anomalies.

    Dimensions: revenue trend by product/service category, cash flow
    pressure, cost growth, customer concentration, abnormal expense patterns.
    """
    raise not_implemented(
        "detect_trends_and_anomalies",
        "run trend/anomaly detection across revenue, cost, and customer "
        "dimensions on the most recently ingested normalized dataset",
    )


@mcp.tool()
def generate_prioritized_recommendations(
    company_id: str, max_items: int = 3
) -> list[Recommendation]:
    """Stage 3: convert detected signals into at most `max_items` recommendations.

    Each recommendation must include a clear action, the reason behind it,
    and a direct reference to the supporting data observation (auditability
    constraint from the proposal's Innovation 4).
    """
    raise not_implemented(
        "generate_prioritized_recommendations",
        "rank detected_signals by urgency/impact and phrase the top "
        "max_items as plain-language action + reason + data reference",
    )


@mcp.tool()
def forecast_revenue(company_id: str, horizon_quarters: int = 1) -> RevenueForecast:
    """Forecast revenue `horizon_quarters` ahead with a confidence interval.

    Intended source: historical revenue trend plus signals from other agents
    (e.g. Marketing campaign pipeline, Operations order backlog).
    """
    raise not_implemented(
        "forecast_revenue",
        "fit a trend model on historical revenue, adjusted by pipeline/"
        "backlog signals from other department agents",
    )


@mcp.tool()
def get_churn_risk_accounts(company_id: str) -> list[ChurnRiskAccount]:
    """List customer accounts at elevated churn risk with the driving signal.

    Intended source: order frequency decline detection over CRM/sales data.
    """
    raise not_implemented(
        "get_churn_risk_accounts",
        "flag accounts whose order frequency has dropped meaningfully over "
        "a trailing window and estimate churn_probability_pct",
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
