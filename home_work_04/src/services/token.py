import uuid
from datetime import datetime, timedelta
from functools import lru_cache
from http import HTTPStatus

import jwt
from fastapi import Depends, HTTPException

from src.core.config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_TOKEN_EXPIRE_MINUTES
from src.db import get_cache

__all__ = ("TokenService", "get_token_service")

from src.db import AbstractCache
from src.services import ServiceMixin

REDIS_REFRESH_TOKEN_BASE_NUM: int = 3
REDIS_AUTH_TOKEN_BASE_NUM: int = 4
JWT_AUTH_TOKEN_EXPIRE_SEC = JWT_TOKEN_EXPIRE_MINUTES * 60
JWT_REFRESH_TOKEN_EXPIRE_SEC = 365 * 24 * 60 * 60

_credentials_exception = HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                                       detail="Could not validate credentials",
                                       headers={"WWW-Authenticate": "Bearer"})


class TokenService(ServiceMixin):

    def logout_all(self, token: dict):
        user_id = token['user_id']

        self.cache.select(REDIS_REFRESH_TOKEN_BASE_NUM)
        key = f"*:{user_id}:*"
        self.cache.delete_by_filter(key)

        self.cache.select(REDIS_AUTH_TOKEN_BASE_NUM)
        self.cache.delete_by_filter(key)

    def logout(self, token: dict):
        user_id = token['user_id']
        refresh_token_id = token['refresh_token_id']
        access_token_id = token['access_token_id']

        self.cache.select(REDIS_REFRESH_TOKEN_BASE_NUM)
        key = f"{refresh_token_id}:{user_id}:{access_token_id}"
        self.cache.delete(key)

        self.cache.select(REDIS_AUTH_TOKEN_BASE_NUM)
        key = f"{access_token_id}:{user_id}:{refresh_token_id}"
        self.cache.delete(key)

    def check_in_cache(self, token: dict) -> bool:
        user_id = token['user_id']
        refresh_token_id = token['refresh_token_id']
        access_token_id = token['access_token_id']
        if token['type'] == 'refresh_token':
            self.cache.select(REDIS_REFRESH_TOKEN_BASE_NUM)
            key = f"{refresh_token_id}:{user_id}:{access_token_id}"
        else:
            self.cache.select(REDIS_AUTH_TOKEN_BASE_NUM)
            key = f"{access_token_id}:{user_id}:{refresh_token_id}"
        if self.cache.get(key) is None:
            return False
        return True

    def refresh_tokens(self, old_refresh_token: dict, check_token_type=True) -> dict:
        if check_token_type and old_refresh_token['type'] != 'refresh_token':
            raise _credentials_exception

        user_id = old_refresh_token['user_id']
        refresh_token_id = old_refresh_token['refresh_token_id']
        access_token_id = old_refresh_token['access_token_id']

        # 1. найдем и удалим старый refresh_token в базе,
        # вдруг его у этого пользователя нет - вызовем исключение
        self.cache.select(REDIS_REFRESH_TOKEN_BASE_NUM)
        key = f"{refresh_token_id}:{user_id}:{access_token_id}"
        if self.cache.get(key) is None:
            raise _credentials_exception
        self.cache.delete(key)

        # 2. удалим старый access_token
        self.cache.select(REDIS_AUTH_TOKEN_BASE_NUM)
        key = f"{access_token_id}:{user_id}:{refresh_token_id}"
        self.cache.delete(key)

        # 3. создадим новые токены
        return self.create_tokens(user_id)

    def create_tokens(self, user_id) -> dict:

        access_token_id = str(uuid.uuid4())
        refresh_token_id = str(uuid.uuid4())

        return {
            "access_token": self.create_access_token(user_id=str(user_id),
                                                     access_token_id=access_token_id,
                                                     refresh_token_id=refresh_token_id),
            "refresh_token": self.create_refresh_token(user_id=str(user_id),
                                                       access_token_id=access_token_id,
                                                       refresh_token_id=refresh_token_id),
            "token_type": "bearer",
        }

    def create_access_token(self, user_id: str, access_token_id: str, refresh_token_id: str) -> str:
        payload = {"type": "access_token",
                   "exp": datetime.utcnow() + timedelta(minutes=JWT_TOKEN_EXPIRE_MINUTES),
                   "iat": datetime.utcnow(),
                   "user_id": user_id,
                   "access_token_id": access_token_id,
                   "refresh_token_id": refresh_token_id}

        token = jwt.encode(payload=payload, key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

        self.cache.select(REDIS_AUTH_TOKEN_BASE_NUM)
        self.cache.set(key=f"{access_token_id}:{user_id}:{refresh_token_id}",
                       value=user_id,
                       expire=JWT_AUTH_TOKEN_EXPIRE_SEC)
        return token

    def create_refresh_token(self, user_id: str, access_token_id: str, refresh_token_id: str) -> str:
        payload = {"type": "refresh_token",
                   "exp": datetime.utcnow() + timedelta(seconds=JWT_REFRESH_TOKEN_EXPIRE_SEC),
                   "iat": datetime.utcnow(),
                   "user_id": user_id,
                   "access_token_id": access_token_id,
                   "refresh_token_id": refresh_token_id}
        token = jwt.encode(payload=payload, key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

        self.cache.select(REDIS_REFRESH_TOKEN_BASE_NUM)
        self.cache.set(key=f"{refresh_token_id}:{user_id}:{access_token_id}",
                       value=token,
                       expire=JWT_REFRESH_TOKEN_EXPIRE_SEC)
        print("\n\n-= CREATE REFRESH TOKEN: ", token)
        return token


# get_token_service — это провайдер PostService. Синглтон
@lru_cache()
def get_token_service(
        cache: AbstractCache = Depends(get_cache),
        session=None,
) -> TokenService:
    return TokenService(cache=cache, session=session)
