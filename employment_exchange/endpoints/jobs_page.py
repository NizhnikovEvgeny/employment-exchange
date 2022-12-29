from fastapi import Depends, APIRouter
from endpoints.depends import get_jobs_page

from models.job_page import JobsPage
from services.get_jobs_page import GetJobsPage

router = APIRouter()


@router.get("/", response_model=JobsPage, response_model_exclude_none=True)
async def get_jobs_page(limit: int = 10, offset: int = 0, jobs_page: GetJobsPage = Depends(get_jobs_page)):
    return await jobs_page(limit=limit, offset=offset)
