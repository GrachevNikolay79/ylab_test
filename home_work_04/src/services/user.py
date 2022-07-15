import json
from functools import lru_cache
from typing import Optional

from fastapi import Depends
from sqlmodel import Session

from src.api.v1.schemas import UserCreate, UserModel
from src.db import AbstractCache, get_cache, get_session
from src.models import User
from src.services import ServiceMixin

__all__ = ("UserService", "get_user_service")


class UserService(ServiceMixin):
    def get_user_list(self) -> dict:
        """Получить список пользователей."""
        users = self.session.query(User).order_by(User.username).all()
        return {"users": [UserModel(**u.dict()) for u in users]}

    def get_user_detail(self, user_id: int) -> Optional[dict]:
        """Получить детальную информацию профиля пользователя."""
        if cached_user := self.cache.get(key=f"{user_id}"):
            return json.loads(cached_user)

        user = self.session.query(User).filter(User.id == user_id).first()
        if user:
            self.cache.set(key=f"{user.id}", value=user.json())
        return user.dict() if user else None

    def create_user(self, user: UserCreate) -> dict:
        """Создать профиль пользователя."""
        new_user = User(username=user.username,
                        email=user.email,
                        password=user.password
                        )
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user.dict()


# get_post_service — это провайдер PostService. Синглтон
@lru_cache()
def get_post_service(
    cache: AbstractCache = Depends(get_cache),
    session: Session = Depends(get_session),
) -> UserService:
    return UserService(cache=cache, session=session)
