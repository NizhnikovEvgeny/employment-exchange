from fastapi import APIRouter, Depends, HTTPException, status
from repositories.users import UserRepository
from .depends import get_user_repository, get_current_user
from typing import List

from models.user import UserIn, User

router = APIRouter()


@router.get("/", response_model=List[User])
async def read_users(
        users: UserRepository = Depends(get_user_repository),
        limit: int = 100,
        offset: int = 0):
    return await users.get_all(limit=limit, offset=offset)


@router.get("/by_id", response_model=User)
async def get_user_by_id(
        id: int,
        users: UserRepository = Depends(get_user_repository)):
    return await users.get_by_id(id=id)


@router.get("/by_email", response_model=User)
async def get_user_by_email(
    email: str,
    users: UserRepository = Depends(get_user_repository)
):
    return await users.get_by_email(email=email)


@router.post("/", response_model=User)
async def create_uses(
    user: UserIn,
    users: UserRepository = Depends(get_user_repository)
):
    return await users.create(user=user)


@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_data: UserIn,
    users: UserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user)
):
    user = await users.get_by_id(id=user_id)
    if user is None or user.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="It's not allowed to update another user")
    return await users.update(id=user_id, user_data=user_data)
