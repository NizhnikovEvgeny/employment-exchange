from pydantic import BaseModel, EmailStr, validator, constr
from typing import Optional
import datetime


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_company: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserBase(User):
    id: Optional[int] = None
    name: Optional[str]
    email: Optional[EmailStr]
    hashed_password: Optional[str]
    is_company: Optional[bool]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class UserIn(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8)
    password2: str
    is_company: bool = False

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values["password"]:
            raise ValueError("passwords don't match")
        return v


class UserJobPageView(BaseModel):
    id: str
    name: str
    email: str
