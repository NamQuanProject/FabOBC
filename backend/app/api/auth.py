"""Demo authentication: pick one of the seeded users, no password.

Matches frontend_temp's login screen (click a user card to "sign in").
Swap for real auth (Supabase Auth, SSO) before any non-demo deployment.
"""

from fastapi import APIRouter, Depends, HTTPException
from supabase import AsyncClient

from app.deps import get_supabase
from app.schema.user import LoginRequest, LoginResponse, UserOut
from app.tables import USERS

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(
    payload: LoginRequest, client: AsyncClient = Depends(get_supabase)
) -> LoginResponse:
    result = (
        await client.table(USERS).select("*").eq("id", payload.user_id).maybe_single().execute()
    )
    if result is None or result.data is None:
        raise HTTPException(status_code=404, detail="Unknown user_id")
    return LoginResponse(user=UserOut(**result.data))
