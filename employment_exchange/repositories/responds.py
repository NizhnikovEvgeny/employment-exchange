import datetime
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from typing import List

from employment_exchange.db.responds import responds
from .base import BaseRepository
from employment_exchange.models.respond import Respond
from employment_exchange.db.responds import responds


class RespondsRepository(BaseRepository):

    async def respond(self, user_id: int, job_id: int) -> Respond:
        new_respond = Respond(
            user_id=user_id,
            job_id=job_id,
            created_at=datetime.datetime.utcnow()
        )
        values = new_respond.dict(exclude_none=True)
        query = insert(responds).values(**values).on_conflict_do_nothing()
        new_respond.id = await self.database.execute(query)
        return Respond.parse_obj(new_respond)

    async def get_responders_by_job_id(self, job_id: int) -> List[int]:
        query = select(responds.c.user_id).select_from(
            responds).where(responds.c.job_id == job_id)
        rows = await self.database.fetch_all(query)
        return list([ids[responds.c.user_id] for ids in rows])
