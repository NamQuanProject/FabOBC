"""MCP tool server for Forge, FabOPC's Operations Agent.

Supplier status, inventory health, order risk, and logistics optimization
tools. See mcp_servers/finance_servers/mcp_server.py for the stub convention.
"""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

from mcp_servers.shared.stub import not_implemented

mcp = FastMCP("fabopc-operations")


class SupplierStatus(BaseModel):
    supplier_name: str
    delay_days: int
    affected_order_count: int
    exposure_vnd: float
    mitigation_plan: str | None = None


class InventoryHealth(BaseModel):
    turnover_ratio: float
    low_buffer_skus: list[str]
    slow_moving_value_vnd: float


class OrderRisk(BaseModel):
    order_id: str
    risk_reason: str  # "supplier_delay" | "carrier_capacity" | other
    estimated_delay_days: int


class LogisticsRecommendation(BaseModel):
    cost_increase_pct: float
    recommended_action: str
    estimated_monthly_savings_vnd: float


@mcp.tool()
def get_supplier_status(company_id: str) -> list[SupplierStatus]:
    """List suppliers currently causing delays, with affected order exposure.

    Intended source: procurement/ERP integration order + supplier tables.
    """
    raise not_implemented(
        "get_supplier_status",
        "join purchase orders with supplier delivery dates to find delays "
        "and sum affected order value",
    )


@mcp.tool()
def get_inventory_health(company_id: str) -> InventoryHealth:
    """Report inventory turnover and flag SKUs below buffer or slow-moving.

    Intended source: inventory/warehouse management integration.
    """
    raise not_implemented(
        "get_inventory_health",
        "compute turnover_ratio from COGS/avg inventory, flag SKUs under "
        "reorder buffer and SKUs with >90d no movement",
    )


@mcp.tool()
def assess_order_risk(company_id: str) -> list[OrderRisk]:
    """List open orders at risk of late delivery and why.

    Intended source: combines get_supplier_status with carrier capacity data.
    """
    raise not_implemented(
        "assess_order_risk",
        "cross-reference open orders against supplier delays and carrier "
        "capacity constraints",
    )


@mcp.tool()
def optimize_logistics(company_id: str) -> LogisticsRecommendation:
    """Recommend a logistics/routing change and estimate monthly savings.

    Intended source: carrier rate history + delivery route data.
    """
    raise not_implemented(
        "optimize_logistics",
        "compare current routing cost per order against alternate carrier/hub "
        "configurations to estimate savings",
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
