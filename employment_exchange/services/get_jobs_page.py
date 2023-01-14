from redis import Redis

from repositories.jobs_page import JobsPageRepository
from repositories.responds import RespondsRepository
from models.job_page import JobsPage, JobPageView
from services.responds_count_cache import RespondsCountCache


class GetJobsPage():
    def __init__(self, jobs_page_repository: JobsPageRepository, responds_repository: RespondsRepository, responds_count_cache: RespondsCountCache) -> None:
        self.jobs_page_repository = jobs_page_repository
        self.responds_repository = responds_repository
        self.responds_count_cache = responds_count_cache

    async def __call__(self, limit: int = 100, offset: int = 0) -> JobsPage:
        jobs = await self.jobs_page_repository.get_jobs(limit=limit, offset=offset)
        not_in_cache_job_ids = []
        # First get counts from cache
        for job in jobs:
            count = await self.responds_count_cache.get_responds_count(job.id)
            if count:
                job.responds_count = count
            else:
                not_in_cache_job_ids.append(job.id)
        # Then get counts from db
        if not not_in_cache_job_ids:
            return JobsPage(jobs=jobs)
        responds_counts = await self.responds_repository.get_jobs_responds_count(jobs_ids=not_in_cache_job_ids)
        for job in jobs:
            count = responds_counts.get(job.id)
            if count is not None:
                job.responds_count = count
                await self.responds_count_cache.set_responds_count(
                    job_id=job.id, count=count)
        return JobsPage(jobs=jobs)
