"""Pydantic result types shared by more than one MCP tool server."""

from pydantic import BaseModel


class TrendPoint(BaseModel):
    label: str
    value: float
    direction: str  # up | down | flat


class SourceCitation(BaseModel):
    """Traceability pointer back to the record a claim was derived from.

    The proposal's auditability constraint (Innovation 4) requires every
    agent-generated claim to be traceable to verified internal data. Tool
    results that make a claim should attach citations pointing at the
    underlying rows/documents once implemented.
    """

    source_table: str
    record_id: str
    field: str | None = None
