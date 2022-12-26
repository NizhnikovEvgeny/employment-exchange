from fastapi import APIRouter, Depends, HTTPException, status

from employment_exchange.repositories.users import UserRepository
from .depends import get_user_repository
from employment_exchange.core.security import hash_password, create_access_token, verify_password
from employment_exchange.models.token import Login, Token
from typing import Optional

router = APIRouter()


@router.post("/", response_model=Token)
async def login(login: Login, users: UserRepository = Depends(get_user_repository)):
    user = await users.get_by_email(email=login.email)
    if user is None or not verify_password(password=login.password, hash=user.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid email or password")
    return Token(
        access_token=create_access_token({"sub": user.email}),
        token_type="Bearer"
    )
