from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import ChatMessage
from app.schema.chat import ChatMessageOut, ChatRequest, ChatResponse
from app.services.orchestrator_service import handle_chat_turn

router = APIRouter(prefix="/api/v1", tags=["chat"])


@router.get(
    "/companies/{company_id}/departments/{department}/messages",
    response_model=list[ChatMessageOut],
)
async def get_chat_history(
    company_id: str, department: str, session: AsyncSession = Depends(get_session)
) -> list[ChatMessageOut]:
    result = await session.execute(
        select(ChatMessage)
        .where(ChatMessage.company_id == company_id, ChatMessage.department == department)
        .order_by(ChatMessage.created_at.asc())
    )
    return [ChatMessageOut.model_validate(m) for m in result.scalars().all()]


@router.post("/agents/orchestrate", response_model=ChatResponse)
async def orchestrate_chat(
    payload: ChatRequest, session: AsyncSession = Depends(get_session)
) -> ChatResponse:
    """Send a chat message to a department's agent (or Orion for 'executive').

    Delegates to app.services.orchestrator_service.handle_chat_turn, which
    persists both sides of the conversation and calls the agent over A2A.
    """
    reply = await handle_chat_turn(
        session=session,
        company_id=payload.company_id,
        user_id=payload.user_id,
        department=payload.department,
        message=payload.message,
    )
    return ChatResponse(department=payload.department, reply=ChatMessageOut.model_validate(reply))
