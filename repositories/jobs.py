import sqlalchemy
from sqlalchemy import Table
import datetime

from .base import BaseRepository
from db.jobs import jobs
from models.job import Job, JobIn
from typing import Optional, List


class JobRepository(BaseRepository):

    async def create_job(self, job_creator_user_id: int, new_job: JobIn) -> Job:
        job = Job(
            user_id=job_creator_user_id,
            title=new_job.title,
            salary_from=new_job.salary_from,
            salary_to=new_job.salary_to,
            is_active=False,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        values = job.dict(exclude_none=True)
        query = jobs.insert().values(**values).returning(jobs.c.created_at,
                                                         jobs.c.title, jobs.c.salary_from)
        row = await self.database.execute(query)
        # row = await rows.fetchone()
        # raise KeyError(f"{row}")
        return Job.parse_obj(row)

    async def get_all_jobs(self, limit: int = 10, offset: int = 0) -> List[Job]:
        query = jobs.select()
        return await self.database.fetch_all(query)
