import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator

__all__ = (
    "UserId",
    "UserModel",
    "UserCreationSchema",
    "UserLoginSchema",
    "UserPatchScheme",
)


class UserId(BaseModel):
    id: str


class UserModel(UserId):
    username: str = Field(min_length=4, max_length=20)
    email: EmailStr
    is_superuser: Optional[bool]
    created_at: Optional[datetime]


class UserCreationSchema(BaseModel):
    username: str = Field(min_length=4, max_length=20)
    email: EmailStr
    is_superuser: Optional[bool]
    created_at: Optional[datetime]
    password: str

    @validator('password')
    def passwords_match(cls, v, values, **kwargs):
        rules = [
            ('password is too short', r'.{5}'),
            ('password needs at least one lower case character', r'[a-z]'),
            # ('password needs at least one upper case character', r'[A-Z]'),
            # ('password needs at least one special character', r'[-_?!@#$%^&*]'),
            ('password needs at least one number', r'[0-9]'),
        ]
        err_msg = ', '.join(req for req, regex in rules if not re.search(regex, v))
        print('\n\n', err_msg)
        assert len(err_msg) < 5, str(err_msg)
        return v

    @validator('username')
    def username_alphanumeric(cls, v: str):
        valid_pattern = re.compile(r"^[a-z0-9 _]+$", re.I)
        assert bool(valid_pattern.match(v)), 'must be num, char, space'
        return v


class UserLoginSchema(BaseModel):
    username: str
    password: str


class UserPatchScheme(BaseModel):
    username: Optional[str] = Field(min_length=4, max_length=20)
    email: Optional[EmailStr]
    password: Optional[str]
