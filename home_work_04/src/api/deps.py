import logging

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from starlette import status
from pydantic import BaseModel
from typing import Optional

from src.api.v1.schemas import UserModel
from src.core.auth import oauth2_scheme
from src.core.config import JWT_SECRET_KEY, JWT_ALGORITHM
from src.services import UserService, get_user_service


class TokenData(BaseModel):
    username: Optional[str] = None


# def get_current_user(token: str = Depends(oauth2_scheme),
def get_current_user(token: str = Depends(HTTPBearer),
                     user_service: UserService = Depends(get_user_service)) -> UserModel:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    log = logging.getLogger()
    log.info("get_current_user()")
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            options={"verify_aud": False},
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.exceptions.PyJWTError:
        raise credentials_exception

    user = user_service.find_user_by_name(username)
    if user is None:
        raise credentials_exception
    return UserModel(**user)
