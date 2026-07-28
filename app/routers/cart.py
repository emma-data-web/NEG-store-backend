from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models import User
from app.schemas.cart import CartItemCreate, CartItemResponse
from app.services.user_services import get_current_user
from app.services.cart_services import (
    add_to_cart,
    get_user_cart,
    update_cart_item,
    remove_cart_item,
)

cart_router = APIRouter()


@cart_router.post("/add-to-cart", response_model=CartItemResponse)
async def create_add_to_cart(
    data: CartItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cart_item = await add_to_cart(
        db=db,
        data=data,
        current_user=current_user,
    )

    return cart_item


@cart_router.get("/my-cart")
async def get_cart(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cart = await get_user_cart(
        db=db,
        current_user=current_user,
    )

    return cart


@cart_router.patch("/cart-item/{cart_item_id}")
async def update_item(
    cart_item_id: int,
    quantity: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await update_cart_item(
        db=db,
        cart_item_id=cart_item_id,
        quantity=quantity,
        current_user=current_user,
    )


@cart_router.delete("/cart-item/{cart_item_id}")
async def remove_item(
    cart_item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await remove_cart_item(
        db=db,
        cart_item_id=cart_item_id,
        current_user=current_user,
    )

    return {
        "message": "Item removed successfully."
    }