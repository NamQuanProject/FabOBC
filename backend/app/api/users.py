from fastapi import APIRouter, Depends, HTTPException
from supabase import AsyncClient

from app.deps import get_supabase
from app.schema.user import UserOut
from app.tables import USERS

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("", response_model=list[UserOut])
async def list_users(client: AsyncClient = Depends(get_supabase)) -> list[UserOut]:
    """List every user — powers the frontend's login screen account picker."""
    result = await client.table(USERS).select("*").execute()
    return [UserOut(**row) for row in result.data]


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: str, client: AsyncClient = Depends(get_supabase)) -> UserOut:
    result = await client.table(USERS).select("*").eq("id", user_id).maybe_single().execute()
    if result is None or result.data is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(**result.data)
