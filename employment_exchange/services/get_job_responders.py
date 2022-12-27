from typing import Optional, List

from employment_exchange.repositories.responds import RespondsRepository
from employment_exchange.repositories.users import UserRepository
from employment_exchange.models.user import User


class GetJobResponders():
    def __init__(self, respond_repository: RespondsRepository, users_repository: UserRepository) -> None:
        self.respond_repository = respond_repository
        self.user_repository = users_repository

    async def __call__(self, job_id: int, limit: int = 100, offset: int = 0) -> List[User]:
        user_ids = await self.respond_repository.get_responders_by_job_id(job_id=job_id)
        users = []
        for id in user_ids:
            users.append(await self.user_repository.get_by_id(id=id))
        return users
