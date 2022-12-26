from fastapi import APIRouter, Depends, HTTPException, status, Response

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
    new_respond = await responds_repository.respond(user_id=current_user.id, job_id=job_id)
    if new_respond is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Couldn't save to DB")
    else:
        return Response(status_code=status.HTTP_201_CREATED)


@router.get("/jobs/{job_id}/responders")
async def get_job_responders(
    limit: int = 10,
    offset: int = 0,
    responds_repository: RespondsRepository = Depends(get_responds_reposotory),

):
    pass
