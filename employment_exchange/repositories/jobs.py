import sqlalchemy
from sqlalchemy import Table
import datetime
from datetime import timezone

from aiopg.sa import SAConnection
from .base import BaseRepository
from employment_exchange.db.jobs import jobs
from employment_exchange.models.job import Job, JobNew, JobBase
from typing import Optional, List


class JobRepository(BaseRepository):

    async def create_job(self, job_creator_user_id: int, new_job: JobNew) -> Job:
        now = datetime.datetime.utcnow()
        job = Job(
            user_id=job_creator_user_id,
            title=new_job.title,
            salary_from=new_job.salary_from,
            salary_to=new_job.salary_to,
            is_active=False,
            created_at=now,
            updated_at=now
        )
        params = job.dict(exclude_none=True)
        query = jobs.insert().values(**params).returning(*jobs.c)
        job_id = await self.database.execute(query)
        job = await self.get_job_by_id(job_id=job_id)
        return Job.parse_obj(job)

    async def update_job(self, job_id: int, job_data: JobBase) -> Job:
        params = job_data.dict(exclude_none=True)
        params.update({"updated_at": datetime.datetime.utcnow()})
        query = jobs.update().values(**params).where(jobs.c.id ==
                                                     job_id).returning(*jobs.c)
        result_proxy = await self.database.execute(query)
        job_id = await result_proxy.fetchone()
        job = await self.get_job_by_id(job_id=job_id)
        return Job.parse_obj(job)

    async def get_all_jobs(self, limit: int = 10, offset: int = 0) -> List[Job]:
        query = jobs.select().order_by(jobs.c.id)
        return await self.database.fetch_all(query)

    async def get_job_by_id(self, job_id: int) -> Job:
        query = jobs.select().where(jobs.c.id == job_id)
        return await self.database.fetch_one(query)
