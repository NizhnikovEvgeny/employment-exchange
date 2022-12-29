import datetime
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, func
from typing import List

from db.responds import responds
from repositories.base import BaseRepository
from models.respond import Respond
from db.responds import responds


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

    async def get_job_responders_count(self, job_id: int) -> int:
        query = select(func.count(responds.c.user_id)
                       ).group_by(responds.c.job_id)
        return int(self.database.fetch_one(query))

    # reutrns a dict of {job_id: responds_count}
    async def get_jobs_responds_count(self, jobs_ids: list[int]) -> dict[int, int]:
        query = select([responds.c.job_id, func.count(responds.c.user_id)]).select_from(
            responds).where(responds.c.job_id.in_(jobs_ids)).group_by(responds.c.job_id)
        rows = await self.database.fetch_all(query)
        jobs_counts = dict.fromkeys(jobs_ids, 0)
        for row in rows:
            jobs_counts[row[responds.c.job_id]] = row[1]
        return jobs_counts
