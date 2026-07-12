from pydantic import BaseModel, ConfigDict


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    company_id: str
    full_name: str
    initials: str
    title: str
    role: str
    department: str
    email: str | None = None


class LoginRequest(BaseModel):
    user_id: str


class LoginResponse(BaseModel):
    user: UserOut
