from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

#from src.api.v1.schemas import UserCreate, UserListResponse, UserModel
#from src.services import UserService, get_user_service
from ..schemas import UserCreate, UserListResponse, UserModel
from src.services import UserService, get_user_service

router = APIRouter()


@router.get(
    path="/",
    response_model=UserListResponse,
    summary="Список пользователей",
    tags=["users"],
)
def user_list(
    user_service: UserService = Depends(get_user_service),
) -> UserListResponse:
    users: dict = user_service.get_user_list()
    if not users:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="users not found")
    return UserListResponse(**users)



@router.get(
    path="/{user_id}",
    response_model=UserModel,
    summary="Получить определенного пользователя",
    tags=["users"],
)
def user_detail(
    user_id: int, user_service: UserService = Depends(get_user_service),
) -> UserModel:
    user: Optional[dict] = user_service.get_user_detail(user_id=user_id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="user not found")
    return UserModel(**user)


@router.post(
    path="/",
    response_model=UserModel,
    summary="Создать учетную запись",
    tags=["users"],
)
def user_create(
    user: UserCreate, user_service: UserService = Depends(get_user_service),
) -> UserModel:
    user: dict = user_service.create_user(user=user)
    return UserModel(**user)
