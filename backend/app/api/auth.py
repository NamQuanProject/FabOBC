"""Demo authentication: pick one of the seeded users, no password.

Matches frontend_temp's login screen (click a user card to "sign in").
Swap for real auth (Supabase Auth, SSO) before any non-demo deployment.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import User
from app.schema.user import LoginRequest, LoginResponse, UserOut

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(
    payload: LoginRequest, session: AsyncSession = Depends(get_session)
) -> LoginResponse:
    result = await session.execute(select(User).where(User.id == payload.user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Unknown user_id")
    return LoginResponse(user=UserOut.model_validate(user))
