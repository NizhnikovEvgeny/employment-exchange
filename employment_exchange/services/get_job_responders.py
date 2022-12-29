from typing import Optional, List

from repositories.responds import RespondsRepository
from repositories.users import UserRepository
from models.user import User


class GetJobResponders():
    def __init__(self, respond_repository: RespondsRepository, users_repository: UserRepository) -> None:
        self.respond_repository = respond_repository
        self.user_repository = users_repository

    async def __call__(self, job_id: int, limit: int = 100, offset: int = 0) -> List[User]:
        user_ids = await self.respond_repository.get_responders_by_job_id(job_id=job_id)
        return await self.user_repository.get_by_ids(ids=user_ids)
