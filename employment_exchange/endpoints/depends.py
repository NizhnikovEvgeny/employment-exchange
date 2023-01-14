from fastapi import Depends, HTTPException, status
from redis import Redis

from repositories.users import UserRepository
from repositories.jobs import JobRepository
from repositories.responds import RespondsRepository
from repositories.jobs_page import JobsPageRepository
from db.base import database
from models.user import User
from core.security import JWTBearer, decode_access_token
from services.get_job_responders import GetJobResponders
from services.get_jobs_page import GetJobsPage
from core.redis import initialize_redis
from services.responds_count_cache import RespondsCountCache


async def get_user_repository() -> UserRepository:
    return UserRepository(database)


async def get_jobs_repository() -> JobRepository:
    return JobRepository(database)


async def get_responds_repository() -> RespondsRepository:
    return RespondsRepository(database)


async def get_jobs_page_repository() -> JobsPageRepository:
    return JobsPageRepository(database)


async def get_redis() -> Redis:
    return await initialize_redis()


async def get_responds_count_cache(redis: Redis = Depends(get_redis)) -> RespondsCountCache:
    return RespondsCountCache(redis=redis)


async def get_job_responders(respond_repository: RespondsRepository = Depends(get_responds_repository), users_repository: UserRepository = Depends(get_user_repository)) -> GetJobResponders:
    return GetJobResponders(respond_repository=respond_repository, users_repository=users_repository)


async def get_jobs_page(jobs_page_repository: JobsPageRepository = Depends(get_jobs_page_repository), responds_repository: RespondsRepository = Depends(get_responds_repository), responds_count_cache: RespondsCountCache = Depends(get_responds_count_cache)) -> GetJobsPage:
    return GetJobsPage(jobs_page_repository=jobs_page_repository, responds_repository=responds_repository, responds_count_cache=responds_count_cache)


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
