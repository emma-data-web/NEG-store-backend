from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.schemas.auth import (
    Message,
    UserCreate,
    UserLogin,
    UserLoginResponse,
    ResetPassword,
    ForgotPassword,
)
from app.services.auth_services import (
    create_user,
    login,
    verify_user_email,
    send_reset_link,
    reset_user_password,
)

auth_router = APIRouter()


@auth_router.post("/register", response_model=Message)
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    await create_user(user=user, db=db)

    return {
        "message": f"Account successfully created. A verification link has been sent to {user.email}."
    }


@auth_router.post("/login", response_model=UserLoginResponse)
async def signin(
    user: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    return await login(user=user, db=db)


@auth_router.get("/verify-email")
async def verify_email(
    token: str,
    db: AsyncSession = Depends(get_db)
):
    user = await verify_user_email(token=token, db=db)

    return {
        "message": f"Email for {user.first_name} was successfully verified."
    }


@auth_router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def request_password_reset(
    request: ForgotPassword,
    db: AsyncSession = Depends(get_db)
):
    return await send_reset_link(
        db=db,
        email=request.email
    )


@auth_router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password_endpoint(
    data: ResetPassword,
    db: AsyncSession = Depends(get_db)
):
    return await reset_user_password(
        db=db,
        data=data
    )