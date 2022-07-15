from datetime import datetime

from pydantic import BaseModel, EmailStr

__all__ = (
    "UserModel",
    "UserCreate",
    "UserListResponse",
)


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserModel(UserBase):
    id: int
    created_at: datetime


class UserListResponse(BaseModel):
    users: list[UserModel] = []
