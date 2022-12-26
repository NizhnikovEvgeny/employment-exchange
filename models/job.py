from pydantic import BaseModel
from typing import Optional
import datetime


class JobBase(BaseModel):
    title: Optional[str]
    salary_from: Optional[int]
    salary_to: Optional[int]
    is_active: Optional[bool]


class Job(JobBase):
    id: int
    user_id: int
    title: str
    is_active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class JobNew(BaseModel):
    title: str
    salary_from: Optional[int]
    salary_to: Optional[int]
