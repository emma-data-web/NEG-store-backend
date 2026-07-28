from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models import User
from app.services.product_services import (
    create_product,
    get_product_by_id,
)
from app.schemas.product import ProductCreate, ProductResponse
from app.services.user_services import get_current_seller


product_router = APIRouter()


@product_router.post("/create-product", response_model=ProductResponse)
async def product_create(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_seller),
):
    print(current_user.role)

    new_product = await create_product(
        db=db,
        data=data,
        current_user=current_user,
    )

    return new_product


@product_router.get("/get-product-by-id/{product_id}")
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
):
    get_prod = await get_product_by_id(
        db=db,
        product_id=product_id,
    )

    return get_prod