from repositories.jobs_page import JobsPageRepository
from repositories.responds import RespondsRepository
from models.job_page import JobsPage, JobPageView


class GetJobsPage():
    def __init__(self, jobs_page_repository: JobsPageRepository, responds_repository: RespondsRepository) -> None:
        self.jobs_page_repository = jobs_page_repository
        self.responds_repository = responds_repository

    async def __call__(self, limit: int = 100, offset: int = 0) -> JobsPage:
        jobs = await self.jobs_page_repository.get_jobs(limit=limit, offset=offset)
        responds_counts = await self.responds_repository.get_jobs_responds_count(jobs_ids=[job.id for job in jobs])
        for job in jobs:
            job.responds_count = responds_counts[job.id]
        return JobsPage(jobs=jobs)
