from models.user import UserJobPageView
from repositories.types import JobPageViewDB

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from pydantic.dataclasses import dataclass


@dataclass
class JobPageView:
    id: int
    title: str
    salary_from: Optional[str]
    salary_to: Optional[str]
    last_updated_at: datetime
    company: UserJobPageView
    responds_count: int = None

    @classmethod
    def from_raw(cls, j: JobPageViewDB):
        return cls(
            id=j.id,
            title=j.title,
            salary_from=j.salary_from,
            salary_to=j.salary_to,
            last_updated_at=j.updated_at,
            company=j.user)


@dataclass
class JobsPage:
    jobs: List[JobPageView]
