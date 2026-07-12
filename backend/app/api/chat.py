from fastapi import APIRouter, Depends
from supabase import AsyncClient

from app.deps import get_supabase
from app.schema.chat import ChatMessageOut, ChatRequest, ChatResponse
from app.services.orchestrator_service import handle_chat_turn
from app.tables import CHAT_MESSAGES

router = APIRouter(prefix="/api/v1", tags=["chat"])


@router.get(
    "/companies/{company_id}/departments/{department}/messages",
    response_model=list[ChatMessageOut],
)
async def get_chat_history(
    company_id: str, department: str, client: AsyncClient = Depends(get_supabase)
) -> list[ChatMessageOut]:
    result = (
        await client.table(CHAT_MESSAGES)
        .select("*")
        .eq("company_id", company_id)
        .eq("department", department)
        .order("created_at")
        .execute()
    )
    return [ChatMessageOut(**row) for row in result.data]


@router.post("/agents/orchestrate", response_model=ChatResponse)
async def orchestrate_chat(
    payload: ChatRequest, client: AsyncClient = Depends(get_supabase)
) -> ChatResponse:
    """Send a chat message to a department's agent (or Orion for 'executive').

    Delegates to app.services.orchestrator_service.handle_chat_turn, which
    persists both sides of the conversation and calls the agent over A2A.
    """
    reply_row = await handle_chat_turn(
        client=client,
        company_id=payload.company_id,
        user_id=payload.user_id,
        department=payload.department,
        message=payload.message,
    )
    return ChatResponse(department=payload.department, reply=ChatMessageOut(**reply_row))
