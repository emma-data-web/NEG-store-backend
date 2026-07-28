from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models.user import User
from app.schemas.user import UserInfoResponse
from app.services.user_services import (
    user_profile,
    delete_user,
    get_current_user,
)

user_router = APIRouter()


@user_router.get("/user-profile/{user_id}", response_model=UserInfoResponse)
async def get_user_profile(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    profile = await user_profile(
        db=db,
        user_id=user_id,
    )

    return profile


@user_router.delete("/delete-user/{user_id}")
async def delete_user_account(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await delete_user(
        user_id=user_id,
        db=db,
        current_user=current_user,
    )

    return {
        "message": "User deleted successfully"
    }