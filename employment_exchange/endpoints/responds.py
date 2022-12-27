from fastapi import APIRouter, Depends, HTTPException, status, Response

from databases import Database

from employment_exchange.repositories.jobs import JobRepository
from employment_exchange.repositories.responds import RespondsRepository
from employment_exchange.models.user import User
from employment_exchange.models.respond import Respond
from employment_exchange.models.job import Job
from .depends import get_current_user, get_jobs_repository, get_responds_reposotory

router = APIRouter()


@router.post("/jobs/{job_id}/respond", status_code=status.HTTP_201_CREATED)
async def respond_on_job(
        job_id: int,
        job_repository: JobRepository = Depends(get_jobs_repository),
        responds_repository: RespondsRepository = Depends(
            get_responds_reposotory),
        current_user: User = Depends(get_current_user)):
    if await job_repository.get_job_by_id(job_id=job_id) is not None:
        await responds_repository.respond(user_id=current_user.id, job_id=job_id)
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job doesn't exist")


@router.get("/jobs/{job_id}/responders")
async def get_job_responders(
    limit: int = 10,
    offset: int = 0,
    responds_repository: RespondsRepository = Depends(get_responds_reposotory),

):
    pass
