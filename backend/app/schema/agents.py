from pydantic import BaseModel


class AgentStatusOut(BaseModel):
    department: str
    persona_name: str
    role_title: str
    online: bool
    url: str
