from typing import List
from sqlalchemy import select

from repositories.base import BaseRepository
from models.job_page import JobPageView
from models.user import UserJobPageView
from repositories.types import JobPageViewDB
from db.jobs import jobs
from db.users import users
import datetime


class JobsPageRepository(BaseRepository):
    users_table = users
    jobs_table = jobs

    async def get_jobs(self, limit: int, offset: int) -> List[JobPageView]:
        query = select([users.c.id, users.c.name, users.c.email, jobs.c.id, jobs.c.title, jobs.c.salary_from, jobs.c.salary_to, jobs.c.updated_at]).select_from(self.users_table).join(self.jobs_table, self.users_table.c.id ==
                                                                                                                                                                                       self.jobs_table.c.user_id).where(self.jobs_table.c.is_active == True).order_by(self.jobs_table.c.updated_at)
        rows = await self.database.fetch_all(query)
        result = []
        for row in rows:
            user = UserJobPageView(
                id=row[users.c.id],
                name=row[users.c.name],
                email=row[users.c.email]
            )
            job = JobPageViewDB(
                id=row[jobs.c.id],
                title=row[jobs.c.title],
                salary_from=row[jobs.c.salary_from],
                salary_to=row[jobs.c.salary_to],
                updated_at=row[jobs.c.updated_at],
                user=user
            )
            result.append(JobPageView.from_raw(job))
        return result
