from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_

from models.user import User, UserIn, UserBase
from repositories.base import BaseRepository
from db.users import users
from core.security import hash_password


class UserRepository(BaseRepository):

    async def get_all(self, limit: int = 10, offset: int = 0) -> List[UserBase]:
        query = users.select().limit(limit).offset(offset)
        return await self.database.fetch_all(query=query)

    async def get_by_id(self, id: int) -> UserBase:
        query = users.select().where(users.c.id == id)
        user = await self.database.fetch_one(query=query)
        return UserBase.parse_obj(user)

    async def get_by_ids(self, ids: list[int]) -> List[UserBase]:
        query = users.select().where(users.c.id.in_(ids))
        return await self.database.fetch_all(query=query)

    async def get_by_email(self, email: str) -> Optional[UserBase]:
        query = users.select().where(users.c.email == email)
        user = await self.database.fetch_one(query=query)
        if user is None:
            return None
        return UserBase.parse_obj(user)

    # Not used
    async def get_by_email_and_hashed_password(self, email: str, hashed_password: str) -> Optional[User]:
        query = users.select().filter(
            and_(users.c.email == email, users.c.hashed_password == hashed_password))
        user = await self.database.fetch_one(query=query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def create(self, user: UserIn) -> User:
        now = datetime.utcnow()
        user = UserBase(
            name=user.name,
            email=user.email,
            hashed_password=hash_password(user.password),
            is_company=user.is_company,
            created_at=now,
            updated_at=now
        )

        values = {**user.dict()}
        values.pop("id", None)

        query = users.insert().values(**values)
        user.id = await self.database.execute(query=query)
        return user

    async def update(self, id: int, user_data: UserIn) -> User:
        now = datetime.utcnow()
        updated_user = User(
            id=id,
            name=user_data.name,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
            is_company=user_data.is_company,
            created_at=now,
            updated_at=now
        )

        values = {**updated_user.dict()}
        values.pop("created_at", None)
        values.pop("id", None)

        query = users.update().where(users.c.id == id).values(**values)
        try:
            await self.database.execute(query=query)
        except:
            raise HTTPException(status_code=500, detail="Database error")
        return updated_user
