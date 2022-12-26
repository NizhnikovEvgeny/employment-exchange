from pydantic import BaseModel
from typing import Optional
import datetime


class Job(BaseModel):
    id: Optional[int] = None
    user_id: int
    title: str
    salary_from: Optional[int]
    salary_to: Optional[int]
    is_active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class JobIn(BaseModel):
    title: str
    salary_from: Optional[int]
    salary_to: Optional[int]
