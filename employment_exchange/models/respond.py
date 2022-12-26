from pydantic import BaseModel
from typing import Optional
import datetime


class Respond(BaseModel):
    id: Optional[str]
    user_id: int
    job_id: int
    created_at: datetime.datetime
