from pydantic.dataclasses import dataclass
from typing import Optional
from datetime import datetime

from models.user import UserJobPageView


@dataclass
class JobPageViewDB:
    id: int
    title: str
    salary_from: Optional[str]
    salary_to: Optional[str]
    updated_at: datetime
    user: UserJobPageView
