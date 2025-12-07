
from pydantic import BaseModel
from sqlalchemy import DECIMAL
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    price: DECIMAL
    description: str | None = None
    quantity: int | None = 0
    category: str | None = None
    image_url: str | None = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    price: DECIMAL | None = None
    description: str | None = None
    quantity: int | None = None
    category: str | None = None
    image_url: str | None = None


class ProductResponse(ProductBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class GetProductResponse(ProductBase):
    id: int
    name: str
    price: float
    description: str

    class Config:
        orm_mode = True
