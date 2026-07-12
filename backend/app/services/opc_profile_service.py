"""CRUD for the persisted OPC Profile Object (opc_profiles.profile JSONB).

Deserializes into core.opc_profile.OPCProfileObject for validation. Agents
mutate this indirectly through the orchestration MCP server's
`update_opc_profile` tool (not yet implemented); this service is what that
tool would eventually call into.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import OPCProfileRecord
from core.opc_profile import CompanyIdentity, OPCProfileObject


async def get_or_create_profile(session: AsyncSession, company_id: str) -> OPCProfileObject:
    result = await session.execute(
        select(OPCProfileRecord).where(OPCProfileRecord.company_id == company_id)
    )
    record = result.scalar_one_or_none()
    if record is None:
        profile = OPCProfileObject(identity=CompanyIdentity(company_id=company_id, legal_name=""))
        record = OPCProfileRecord(company_id=company_id, profile=profile.model_dump(mode="json"))
        session.add(record)
        await session.commit()
        await session.refresh(record)
        return profile
    return OPCProfileObject.model_validate(record.profile)


async def save_profile(
    session: AsyncSession, company_id: str, profile: OPCProfileObject
) -> OPCProfileObject:
    result = await session.execute(
        select(OPCProfileRecord).where(OPCProfileRecord.company_id == company_id)
    )
    record = result.scalar_one_or_none()
    if record is None:
        record = OPCProfileRecord(company_id=company_id)
        session.add(record)
    record.profile = profile.model_dump(mode="json")
    await session.commit()
    return profile
