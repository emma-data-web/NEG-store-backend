from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.security import bearer_scheme
from app.dependencies import get_db
from app.core.config import Settings
from app.models.user import User


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            Settings.SECRET_KEY,
            algorithms=[Settings.JWT_ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    stmt = (
        select(User)
        .options(selectinload(User.store))
        .where(User.id == int(user_id))
    )

    result = await db.execute(stmt)

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User no longer exists",
        )

    return user


async def get_current_admin(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only"
        )

    return current_user


async def get_current_seller(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "seller":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sellers only"
        )

    return current_user


async def user_profile(
    db: AsyncSession,
    user_id: int
):
    stmt = select(User).where(User.id == user_id)

    result = await db.execute(stmt)

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


async def delete_user(
    db: AsyncSession,
    user_id: int,
    current_user: User
):
    stmt = select(User).where(User.id == user_id)

    result = await db.execute(stmt)

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User does not exist"
        )

    if user.id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorised to delete this account"
        )

    await db.delete(user)
    await db.commit()

    return {"message": "User deleted"}