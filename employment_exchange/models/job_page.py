from pydantic import BaseModel


class JobsPage(BaseModel):
    jobs: list[JobView]


class JobView(BaseModel):
    id: int
