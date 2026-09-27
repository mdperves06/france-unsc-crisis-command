from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from app.models.user import UserRole


# ── Request Schemas ──────────────────────────────────────────
class UserRegister(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str = Field(min_length=8)
    country_assignment: Optional[str] = "France"
    role: Optional[UserRole] = UserRole.STUDENT


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)


# ── Response Schemas ─────────────────────────────────────────
class UserOut(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    role: UserRole
    country_assignment: str
    is_active: bool
    is_verified: bool
    avatar_url: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class AuthStatus(BaseModel):
    authenticated: bool
    user: Optional[UserOut] = None
