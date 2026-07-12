from datetime import datetime

from pydantic import BaseModel, ConfigDict


class KpiOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    department: str
    label: str
    value: str
    trend_label: str | None = None
    trend_direction: str | None = None


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    department: str
    title: str
    status: str
    due_label: str | None = None
    created_at: datetime


class DepartmentDashboard(BaseModel):
    department: str
    agent_persona: str
    agent_role_title: str
    insight: str
    kpis: list[KpiOut]
    tasks: list[TaskOut]


class KnowledgeSourceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    source_type: str
    indexed: bool


class BusinessProfileOut(BaseModel):
    company_id: str
    legal_name: str
    industry: str | None
    tax_id: str | None
    employee_count: int | None
    annual_revenue_vnd: float | None
    digital_maturity_level: int | None
    knowledge_sources: list[KnowledgeSourceOut]
