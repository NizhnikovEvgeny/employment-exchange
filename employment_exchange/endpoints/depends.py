from fastapi import Depends, HTTPException, status

from employment_exchange.repositories.users import UserRepository
from employment_exchange.repositories.jobs import JobRepository
from employment_exchange.repositories.responds import RespondsRepository
from employment_exchange.db.base import database
from employment_exchange.models.user import User
from employment_exchange.core.security import JWTBearer, decode_access_token


def get_user_repository() -> UserRepository:
    return UserRepository(database)


def get_jobs_repository() -> JobRepository:
    return JobRepository(database)


def get_responds_reposotory() -> RespondsRepository:
    return RespondsRepository(database)


async def get_current_user(
    users: UserRepository = Depends(get_user_repository),
    token: str = Depends(JWTBearer())
) -> User:
    cred_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception
    email: str = payload.get("sub")
    if email is None:
        raise cred_exception
    user = await users.get_by_email(email=email)
    if user is None:
        raise cred_exception
    return user