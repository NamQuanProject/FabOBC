from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import Company, DepartmentKPI, DepartmentTask, KnowledgeSource
from app.schema.department import (
    BusinessProfileOut,
    DepartmentDashboard,
    KnowledgeSourceOut,
    KpiOut,
    TaskOut,
)
from core.personas import PERSONAS

router = APIRouter(prefix="/api/v1", tags=["departments"])


@router.get("/companies/{company_id}/departments/{department}", response_model=DepartmentDashboard)
async def get_department_dashboard(
    company_id: str, department: str, session: AsyncSession = Depends(get_session)
) -> DepartmentDashboard:
    """KPIs + active tasks for one department, plus its agent persona/insight.

    The `insight` line is currently the persona's static welcome_line; once
    the BI agent's generate_prioritized_recommendations tool is implemented,
    this should surface that department's latest recommendation instead.
    """
    persona = PERSONAS.get(department)
    if persona is None:
        raise HTTPException(status_code=404, detail="Unknown department")

    kpi_result = await session.execute(
        select(DepartmentKPI).where(
            DepartmentKPI.company_id == company_id, DepartmentKPI.department == department
        )
    )
    task_result = await session.execute(
        select(DepartmentTask).where(
            DepartmentTask.company_id == company_id, DepartmentTask.department == department
        )
    )

    return DepartmentDashboard(
        department=department,
        agent_persona=persona.name,
        agent_role_title=persona.role_title,
        insight=persona.welcome_line,
        kpis=[KpiOut.model_validate(k) for k in kpi_result.scalars().all()],
        tasks=[TaskOut.model_validate(t) for t in task_result.scalars().all()],
    )


@router.get("/companies/{company_id}/business-profile", response_model=BusinessProfileOut)
async def get_business_profile(
    company_id: str, session: AsyncSession = Depends(get_session)
) -> BusinessProfileOut:
    result = await session.execute(select(Company).where(Company.id == company_id))
    company = result.scalar_one_or_none()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    sources_result = await session.execute(
        select(KnowledgeSource).where(KnowledgeSource.company_id == company_id)
    )

    return BusinessProfileOut(
        company_id=company.id,
        legal_name=company.legal_name,
        industry=company.industry,
        tax_id=company.tax_id,
        employee_count=company.employee_count,
        annual_revenue_vnd=company.annual_revenue_vnd,
        digital_maturity_level=company.digital_maturity_level,
        knowledge_sources=[
            KnowledgeSourceOut.model_validate(s) for s in sources_result.scalars().all()
        ],
    )
