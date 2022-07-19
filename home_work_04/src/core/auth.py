import time
from http import HTTPStatus
from typing import Optional, Union

import jwt
from fastapi import Depends, Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.api.v1.schemas import UserModel
from src.core.config import JWT_SECRET_KEY, JWT_ALGORITHM
from src.core.security import verify_password
from src.services import UserService, get_user_service
from src.services.token import get_token_service, TokenService


def authenticate(username: str, password: str, user_service: UserService) -> Optional[UserModel]:
    user: dict = user_service.find_user_by_name(username)
    if not user:
        return None
    if not verify_password(password, user['password']):
        return None
    return UserModel(**user)


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request, token_service: TokenService = Depends(get_token_service)):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")

            if (token_dict := decode_token(credentials.credentials)) is None:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            if not token_service.check_in_cache(token_dict):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")

            return token_dict
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")


# def decode_token(token: str, token_service: TokenService = Depends(get_token_service)) -> Union[dict, None]:
def decode_token(token: str) -> Union[dict, None]:
    try:
        dt = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        if int(dt["exp"]) > int(time.time()):
            return dt
        return None
    except jwt.exceptions.PyJWTError:
        return None


def get_current_user(token: dict = Depends(JWTBearer()),
                     user_service: UserService = Depends(get_user_service),
                     ) -> UserModel:
    credentials_exception = HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    try:
        if (user_id := token.get("user_id")) is None:
            raise credentials_exception
    except jwt.exceptions.PyJWTError:
        raise credentials_exception

    user = user_service.find_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    return UserModel(**user)


def get_current_user_id(token: dict = Depends(JWTBearer()),
                        ) -> str:
    credentials_exception = HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    try:
        if (user_id := token.get("user_id")) is None:
            raise credentials_exception
    except jwt.exceptions.PyJWTError:
        raise credentials_exception

    return user_id
