import json
import time
import uuid
from functools import lru_cache
from typing import Optional

from fastapi import Depends
from sqlmodel import Session

from src.api.v1.schemas import UserCreationSchema, UserModel, UserPatchScheme
from src.core.config import CACHE_EXPIRE_IN_SECONDS
from src.core.security import get_password_hash
from src.db import AbstractCache, get_cache, get_session
from src.models.user import User
from src.services import ServiceMixin

__all__ = ("UserService", "get_user_service")

REDIS_USER_BASE_NUM: int = 2


class UserService(ServiceMixin):
    def __get_user_list(self) -> dict:
        """Получить список пользователей."""
        users = self.session.query(User).order_by(User.id).all()
        return {"users": [UserModel(**u.dict()) for u in users]}

    # по сути это одно и тоже, хотя предполагалось что в одном случае достаточно только ID
    # а в другом надо получать всё
    def get_user_detail_by_id(self, user_id: str) -> Optional[dict]:
        if cached_usr := self.__get_user_from_cache_by_id(user_id):
            return cached_usr
        user = self.session.query(User).filter(User.id == user_id).first()
        self.__set_user_cache(user)
        return user.dict() if user else None

    def find_user_by_id(self, user_id: str) -> Optional[dict]:
        if cached_usr := self.__get_user_from_cache_by_id(user_id):
            return cached_usr
        user = self.session.query(User).filter(User.id == user_id).first()
        self.__set_user_cache(user)
        return user.dict() if user else None

    # по сути это одно и тоже, хотя предполагалось что в одном случае достаточно только ID
    # а в другом надо получать всё
    def get_user_detail_by_name(self, name: str) -> Optional[dict]:
        if cached_usr := self.__get_user_from_cache_by_name(name):
            return cached_usr
        user = self.session.query(User).filter(User.username == name).first()
        self.__set_user_cache(user)
        return user.dict() if user else None

    def find_user_by_name(self, name: str) -> Optional[dict]:
        if cached_usr := self.__get_user_from_cache_by_name(name):
            return cached_usr
        # user = self.session.query(User).filter(User.username == name).options(load_only("id")).first()
        user = self.session.query(User).filter(User.username == name).first()
        self.__set_user_cache(user)
        return user.dict() if user else None

    def find_user_by_email(self, email: str) -> Optional[dict]:
        # user = self.session.query(User).filter(User.username == name).options(load_only("id")).first()
        user = self.session.query(User).filter(User.email == email).first()
        self.__set_user_cache(user)
        return user.dict() if user else None

    #
    #
    def create_user(self, user: UserCreationSchema) -> dict:
        """Создать профиль пользователя."""
        # User - models.user
        default = str(uuid.uuid1(clock_seq=time.time_ns()))
        new_user = User(id=default,
                        username=user.username,
                        email=user.email,
                        password=get_password_hash(user.password),
                        is_superuser=user.is_superuser
                        )
        # self.session.query(User).filter(User.id == id).first()
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        self.__set_user_cache(new_user)
        return new_user.dict()

    #
    #
    def patch_user(self, new_user: UserPatchScheme, current_user_id: str) -> dict:
        user = self.session.query(User).filter(User.id == current_user_id).first()
        if new_user.username is not None:
            user.username = new_user.username
        if new_user.email is not None:
            user.email = new_user.email
        if new_user.password is not None:
            user.password = get_password_hash(new_user.password)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        self.__set_user_cache(user)
        return user.dict()

    #
    #
    def __set_user_cache(self, user: User):
        if user:
            self.cache.select(REDIS_USER_BASE_NUM)
            self.cache.set(key=f"{user.id}", value=user.json(), expire=CACHE_EXPIRE_IN_SECONDS)
            self.cache.set(key=f"{user.username}", value=user.id, expire=CACHE_EXPIRE_IN_SECONDS)

    def __get_user_from_cache_by_id(self, user_id: str) -> Optional[dict]:
        self.cache.select(REDIS_USER_BASE_NUM)
        if cached_usr := self.cache.get(key=f"{user_id}"):
            return json.loads(cached_usr)
        return None

    def __get_user_from_cache_by_name(self, name: str) -> Optional[dict]:
        self.cache.select(REDIS_USER_BASE_NUM)
        if cached_usr_id := self.cache.get(key=f"{name}"):
            if cached_usr := self.cache.get(key=f"{cached_usr_id}"):
                return json.loads(cached_usr)
        return None


# get_post_service — это провайдер PostService. Синглтон
@lru_cache()
def get_user_service(
        cache: AbstractCache = Depends(get_cache),
        session: Session = Depends(get_session),
) -> UserService:
    return UserService(cache=cache, session=session)
