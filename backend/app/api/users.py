from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import User
from app.schema.user import UserOut

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("", response_model=list[UserOut])
async def list_users(session: AsyncSession = Depends(get_session)) -> list[UserOut]:
    """List every user — powers the frontend's login screen account picker."""
    result = await session.execute(select(User))
    return [UserOut.model_validate(u) for u in result.scalars().all()]


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: str, session: AsyncSession = Depends(get_session)) -> UserOut:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut.model_validate(user)
