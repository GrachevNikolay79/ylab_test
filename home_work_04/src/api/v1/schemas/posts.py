from datetime import datetime
from typing import Optional

from pydantic import BaseModel

__all__ = (
    "PostModel",
    "PostCreate",
    "PostListResponse",
)


class PostBase(BaseModel):
    title: str
    description: str
    author_id: Optional[str]


class PostCreate(PostBase):
    ...


class PostModel(PostBase):
    id: int
    created_at: datetime


class PostListResponse(BaseModel):
    posts: list[PostModel] = []
