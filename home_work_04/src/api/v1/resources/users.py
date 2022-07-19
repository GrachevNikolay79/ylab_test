from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Body

from src.api.v1.schemas import UserCreationSchema, UserModel, UserLoginSchema, UserPatchScheme
from src.core.auth import authenticate, get_current_user, JWTBearer
from src.services import UserService, get_user_service
from src.services.token import get_token_service, TokenService

user_router = APIRouter()


#
#    SignUp user
#
@user_router.post(path="/signup",
                  response_model=UserModel,
                  summary="Создать учетную запись",
                  tags=["users"],
                  status_code=HTTPStatus.CREATED)
def user_create(user: UserCreationSchema, user_service: UserService = Depends(get_user_service)) -> UserModel:
    if user_service.find_user_by_name(user.username):
        raise HTTPException(status_code=400,
                            detail="The user with this username already exists in the system")
    if user_service.find_user_by_email(user.email):
        raise HTTPException(status_code=400,
                            detail="The user with this email already exists in the system")
    user: dict = user_service.create_user(user=user)
    return UserModel(**user)


#
#    LogIn
#
@user_router.post(path="/login",
                  response_model=dict,
                  summary="Войти в учетную запись",
                  tags=["users"],
                  status_code=HTTPStatus.OK)
async def user_login(user: UserLoginSchema = Body(...),
                     user_service: UserService = Depends(get_user_service),
                     token_service: TokenService = Depends(get_token_service)):
    user_ = authenticate(username=user.username, password=user.password, user_service=user_service)
    if not user_:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return token_service.create_tokens(user_id=str(user_.id))


#
#    See own profile
#
@user_router.get(path="/users/me",
                 response_model=UserModel,
                 summary="Получить информацию о себе",
                 tags=["users"],
                 )
def read_users_me(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    return current_user


#
#    Refresh token
#
@user_router.post(path="/refresh",
                  response_model=dict,
                  summary="Обновить токен",
                  tags=["users"],
                  status_code=HTTPStatus.OK)
def refresh_token(refresh_token_: dict = Depends(JWTBearer()),
                  token_service: TokenService = Depends(get_token_service)) -> dict:
    return token_service.refresh_tokens(refresh_token_)


#
#    Patch own profile
#
@user_router.patch(path="/users/me",
                   response_model=dict,
                   summary="Изменить учетную запись",
                   tags=["users"],
                   status_code=HTTPStatus.OK)
def user_patch(user: UserPatchScheme,
               token: dict = Depends(JWTBearer()),
               user_service: UserService = Depends(get_user_service),
               token_service: TokenService = Depends(get_token_service)
               ) -> dict:
    current_user_id = token['user_id']
    u = user_service.patch_user(user, current_user_id)
    u['uuid'] = current_user_id
    ret = token_service.refresh_tokens(old_refresh_token=token, check_token_type=False)
    ret["user"] = u
    return ret


#
#    LogOut
#
@user_router.post(path="/logout",
                  response_model=dict,
                  summary="Выйти из учетной записи",
                  tags=["users"],
                  status_code=HTTPStatus.OK)
def user_logout(token: dict = Depends(JWTBearer()),
                token_service: TokenService = Depends(get_token_service)):
    token_service.logout(token)


#
#    Logout all devices
#
@user_router.post(path="/logout_all",
                  response_model=dict,
                  summary="Выйти из всех устройств",
                  tags=["users"],
                  status_code=HTTPStatus.OK)
def user_logout(token: dict = Depends(JWTBearer()),
                token_service: TokenService = Depends(get_token_service)):
    token_service.logout_all(token)
