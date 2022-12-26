from pydantic import BaseModel, EmailStr
from typing import Optional
from fastapi import HTTPException


class Token(BaseModel):
    access_token: str
    token_type: str


class Login(BaseModel):
    email: EmailStr
    password: str
