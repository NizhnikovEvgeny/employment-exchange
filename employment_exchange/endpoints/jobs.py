from fastapi import APIRouter, HTTPException, status
from typing import List, Optional

from models.job import JobNew, Job, JobBase
from models.user import User
from repositories.jobs import JobRepository
from repositories.users import UserRepository
from .depends import Depends, get_jobs_repository, get_current_user, get_user_repository

router = APIRouter()


@router.post("/", response_model=Job)
async def create_job(
        new_job: JobNew,
        job_repository: JobRepository = Depends(get_jobs_repository),
        user_repository: UserRepository = Depends(get_user_repository),
        current_user: User = Depends(get_current_user)) -> Job:
    if current_user.is_company == True:
        return await job_repository.create_job(job_creator_user_id=current_user.id, new_job=new_job)
    else:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="Only companies can create jobs")


@router.get("/", response_model=List[Job])
async def get_all_jobs(
        limit: int = 100,
        offset: int = 0,
        job_repository: JobRepository = Depends(get_jobs_repository)):
    return await job_repository.get_all_jobs(limit=limit, offset=offset)


@router.get("/{job_id}", response_model=Job)
async def get_job_by_id(
        job_id: int,
        job_repository: JobRepository = Depends(get_jobs_repository)):
    job = await job_repository.get_job_by_id(job_id=job_id)
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job does not exist")
    return job


@router.patch("/{job_id}", response_model=Job)
async def update_job(
        job_data: JobBase,
        job_id: int,
        job_repository: JobRepository = Depends(get_jobs_repository),
        current_user: User = Depends(get_current_user)):
    old_job = await job_repository.get_job_by_id(job_id=job_id)
    if old_job.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Only owners can update jobs")
    return await job_repository.update_job(job_id=job_id, job_data=job_data)
