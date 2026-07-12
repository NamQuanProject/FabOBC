"""MCP tool server for Nova, FabOPC's Marketing Agent.

Content drafting, campaign analytics, calendar planning, and audience
segmentation tools. See mcp_servers/finance_servers/mcp_server.py for the
stub-implementation convention used throughout this file.
"""

from datetime import date

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

from mcp_servers.shared.stub import not_implemented

mcp = FastMCP("fabopc-marketing")


class ContentDraft(BaseModel):
    channel: str  # facebook | zalo | linkedin | email
    language: str  # "vi" | "en" | "bilingual"
    body: str
    tone: str


class CampaignPerformance(BaseModel):
    window_days: int
    reach: int
    engagement_pct: float
    leads: int
    cost_per_acquisition_vnd: float
    top_campaign_name: str


class ScheduledPost(BaseModel):
    day_label: str
    channel: str
    summary: str


class AudienceSegment(BaseModel):
    segment_name: str
    lead_to_deal_pct: float
    relative_engagement: float  # multiple of baseline, e.g. 2.3x -> 2.3


@mcp.tool()
def draft_social_content(company_id: str, channel: str, brief: str) -> ContentDraft:
    """Draft on-brand social content for `channel` from a short brief.

    Intended source: company voice/brand guidelines from knowledge_sources
    plus recent high-performing post patterns from get_campaign_performance.
    """
    raise not_implemented(
        "draft_social_content",
        "generate channel-appropriate bilingual copy using the company's "
        "knowledge base and historical top-performing content as style guide",
    )


@mcp.tool()
def get_campaign_performance(company_id: str, window_days: int = 30) -> CampaignPerformance:
    """Summarize reach/engagement/leads/CAC across channels over the window.

    Intended source: connected ad platform + CRM integrations.
    """
    raise not_implemented(
        "get_campaign_performance",
        "aggregate per-channel ad platform metrics and CRM lead attribution "
        "over the trailing window_days",
    )


@mcp.tool()
def plan_content_calendar(company_id: str, week_start: date) -> list[ScheduledPost]:
    """Propose a content calendar for the week starting `week_start`.

    Intended source: content cadence rules from the OPC Profile Object plus
    upcoming business events (promotions, compliance deadlines) from other
    agents' shared context.
    """
    raise not_implemented(
        "plan_content_calendar",
        "propose one post per active channel per week using cadence rules "
        "and any upcoming events surfaced by other agents",
    )


@mcp.tool()
def analyze_audience_segments(company_id: str) -> list[AudienceSegment]:
    """Rank audience segments by conversion and engagement.

    Intended source: CRM deal data joined with ad platform audience data.
    """
    raise not_implemented(
        "analyze_audience_segments",
        "join CRM lead-to-deal conversion with ad platform engagement by "
        "audience segment, rank descending by lead_to_deal_pct",
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
