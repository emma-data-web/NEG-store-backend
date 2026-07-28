from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.schemas.store import StoreResponse, CreateStore, StoreUpdate
from app.services.store_services import (
    create_store,
    update_store,
    delete_store,
)
from app.services.user_services import (
    get_current_user,
    get_current_seller,
)
from app.models.user import User


store_router = APIRouter()


@store_router.post("/create-store", response_model=StoreResponse)
async def store(
    data: CreateStore,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_store = await create_store(
        db=db,
        data=data,
        current_user=current_user,
    )

    return new_store


@store_router.put("/update-store/{store_id}")
async def store_update(
    store_id: int,
    data: StoreUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_seller),
):
    updated_store = await update_store(
        db=db,
        store_id=store_id,
        data=data,
        current_user=current_user,
    )

    return updated_store


@store_router.delete("/delete-store/{store_id}")
async def delete_stores(
    store_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_seller),
):
    await delete_store(
        db=db,
        store_id=store_id,
        current_user=current_user,
    )

    return {
        "message": "Store deleted successfully"
    }