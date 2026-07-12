"""Business logic tying the chat API to the A2A agent layer + chat history.

Structure only for the agent-call path (depends on the not-yet-implemented
MCP tool bodies), but the persistence path (saving both sides of the
conversation) is fully wired so the frontend chat UI has something real to
render even before agent tool logic is implemented — see
app/api/chat.py.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ChatMessage
from app.services.a2a_client import send_message_to_agent


async def handle_chat_turn(
    session: AsyncSession,
    company_id: str,
    user_id: str,
    department: str,
    message: str,
) -> ChatMessage:
    """Persist the user's message, call the department's agent, persist + return the reply."""
    user_message = ChatMessage(
        company_id=company_id,
        user_id=user_id,
        department=department,
        sender="user",
        content=message,
    )
    session.add(user_message)
    await session.flush()

    try:
        reply_text = await send_message_to_agent(department, message)
    except Exception as exc:  # noqa: BLE001 - surface as a chat message, not a 500
        reply_text = (
            "This agent's tools aren't implemented yet, so I can't answer that "
            f"for real. (internal: {exc})"
        )

    agent_message = ChatMessage(
        company_id=company_id,
        user_id=user_id,
        department=department,
        sender="agent",
        content=reply_text,
    )
    session.add(agent_message)
    await session.commit()
    await session.refresh(agent_message)
    return agent_message
