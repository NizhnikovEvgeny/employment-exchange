from fastapi import APIRouter, Depends, HTTPException, status, Response, BackgroundTasks
from typing import List

from repositories.jobs import JobRepository
from repositories.responds import RespondsRepository
from models.user import User
from .depends import get_current_user, get_jobs_repository, get_responds_repository, get_job_responders, get_responds_count_cache
from services.get_job_responders import GetJobResponders
from services.responds_count_cache import RespondsCountCache

router = APIRouter()


@router.post("/jobs/{job_id}/respond", status_code=status.HTTP_201_CREATED)
async def respond_on_job(
        job_id: int,
        backgroud_tasks: BackgroundTasks,
        job_repository: JobRepository = Depends(get_jobs_repository),
        responds_repository: RespondsRepository = Depends(
            get_responds_repository),
        current_user: User = Depends(get_current_user),
        responds_count_cache: RespondsCountCache = Depends(get_responds_count_cache)):
    if await job_repository.get_job_by_id(job_id=job_id) is not None:
        await responds_repository.respond(user_id=current_user.id, job_id=job_id)
        backgroud_tasks.add_task(
            responds_count_cache.increment_if_exists, job_id)
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job doesn't exist")


@router.get("/jobs/{job_id}/responders")
async def get_job_responders(
        job_id: int,
        limit: int = 10,
        offset: int = 0,
        get_job_responders: GetJobResponders = Depends(get_job_responders)):
    return await get_job_responders(job_id=job_id, limit=limit, offset=offset)
