from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ChatMessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    department: str
    sender: str
    content: str
    created_at: datetime


class ChatRequest(BaseModel):
    company_id: str
    user_id: str
    department: str
    message: str


class ChatResponse(BaseModel):
    department: str
    reply: ChatMessageOut
