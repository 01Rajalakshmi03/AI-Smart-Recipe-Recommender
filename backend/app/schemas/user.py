from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: str
    full_name: str = ""


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str = ""


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    full_name: str | None = None
    avatar: str | None = None
    dark_mode: bool | None = None


class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    avatar: str
    dark_mode: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class PasswordChange(BaseModel):
    current_password: str
    new_password: str
