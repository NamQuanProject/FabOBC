from fastapi import APIRouter, Depends, HTTPException
from supabase import AsyncClient

from app.deps import get_supabase
from app.schema.department import (
    BusinessProfileOut,
    DepartmentDashboard,
    KnowledgeSourceOut,
    KpiOut,
    TaskOut,
)
from app.tables import COMPANIES, DEPARTMENT_KPIS, DEPARTMENT_TASKS, KNOWLEDGE_SOURCES
from core.personas import PERSONAS

router = APIRouter(prefix="/api/v1", tags=["departments"])


@router.get("/companies/{company_id}/departments/{department}", response_model=DepartmentDashboard)
async def get_department_dashboard(
    company_id: str, department: str, client: AsyncClient = Depends(get_supabase)
) -> DepartmentDashboard:
    """KPIs + active tasks for one department, plus its agent persona/insight.

    The `insight` line is currently the persona's static welcome_line; once
    the BI agent's generate_prioritized_recommendations tool is implemented,
    this should surface that department's latest recommendation instead.
    """
    persona = PERSONAS.get(department)
    if persona is None:
        raise HTTPException(status_code=404, detail="Unknown department")

    kpi_result = (
        await client.table(DEPARTMENT_KPIS)
        .select("*")
        .eq("company_id", company_id)
        .eq("department", department)
        .execute()
    )
    task_result = (
        await client.table(DEPARTMENT_TASKS)
        .select("*")
        .eq("company_id", company_id)
        .eq("department", department)
        .order("created_at")
        .execute()
    )

    return DepartmentDashboard(
        department=department,
        agent_persona=persona.name,
        agent_role_title=persona.role_title,
        insight=persona.welcome_line,
        kpis=[KpiOut(**row) for row in kpi_result.data],
        tasks=[TaskOut(**row) for row in task_result.data],
    )


@router.get("/companies/{company_id}/business-profile", response_model=BusinessProfileOut)
async def get_business_profile(
    company_id: str, client: AsyncClient = Depends(get_supabase)
) -> BusinessProfileOut:
    company_result = (
        await client.table(COMPANIES).select("*").eq("id", company_id).maybe_single().execute()
    )
    if company_result is None or company_result.data is None:
        raise HTTPException(status_code=404, detail="Company not found")
    company = company_result.data

    sources_result = (
        await client.table(KNOWLEDGE_SOURCES).select("*").eq("company_id", company_id).execute()
    )

    return BusinessProfileOut(
        company_id=company["id"],
        legal_name=company["legal_name"],
        industry=company.get("industry"),
        tax_id=company.get("tax_id"),
        employee_count=company.get("employee_count"),
        annual_revenue_vnd=company.get("annual_revenue_vnd"),
        digital_maturity_level=company.get("digital_maturity_level"),
        knowledge_sources=[KnowledgeSourceOut(**row) for row in sources_result.data],
    )
