from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.services.opc_profile_service import get_or_create_profile
from core.opc_profile import OPCProfileObject

router = APIRouter(prefix="/api/v1", tags=["opc-profile"])


@router.get("/companies/{company_id}/opc-profile", response_model=OPCProfileObject)
async def get_opc_profile(
    company_id: str, session: AsyncSession = Depends(get_session)
) -> OPCProfileObject:
    """Read the shared OPC Profile Object (Innovation 1) for `company_id`."""
    return await get_or_create_profile(session, company_id)
