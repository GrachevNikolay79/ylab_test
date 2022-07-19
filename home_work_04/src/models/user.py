from datetime import datetime
from typing import List

from sqlmodel import Field, SQLModel, Relationship

# from src.models.post import Post
__all__ = ("User")


class User(SQLModel, table=True):
    id: str = Field(primary_key=True, nullable=False, max_length=36)
    username: str = Field(nullable=False, index=True)
    email: str = Field(nullable=False)
    password: str = Field(nullable=False)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    is_superuser: bool = Field(default=False, nullable=False)

    posts: List['Post'] = Relationship(back_populates="author")
