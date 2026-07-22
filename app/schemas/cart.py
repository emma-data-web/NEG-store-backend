from pydantic import BaseModel
from datetime import datetime


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemResponse(BaseModel):
    id: int
    cart_id: int
    product_id: int
    quantity: int
    created_at: datetime

    class Config:
        from_attributes = True