import datetime

from employment_exchange.db.responds import responds
from .base import BaseRepository
from employment_exchange.models.respond import Respond
from employment_exchange.db.responds import responds


class RespondsRepository(BaseRepository):

    async def respond(self, user_id: int, job_id: int) -> Respond:
        new_respond = Respond(
            user_id=user_id,
            job_id=job_id,
            created_at=datetime.datetime.utcnow()
        )
        values = new_respond.dict(exclude_none=True)
        query = responds.insert().values(**values)
        new_respond.id = await self.database.execute(query)
        return Respond.parse_obj(new_respond)
