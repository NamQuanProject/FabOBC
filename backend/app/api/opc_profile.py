from fastapi import APIRouter, Depends
from supabase import AsyncClient

from app.deps import get_supabase
from app.services.opc_profile_service import get_or_create_profile
from core.opc_profile import OPCProfileObject

router = APIRouter(prefix="/api/v1", tags=["opc-profile"])


@router.get("/companies/{company_id}/opc-profile", response_model=OPCProfileObject)
async def get_opc_profile(
    company_id: str, client: AsyncClient = Depends(get_supabase)
) -> OPCProfileObject:
    """Read the shared OPC Profile Object (Innovation 1) for `company_id`."""
    return await get_or_create_profile(client, company_id)
