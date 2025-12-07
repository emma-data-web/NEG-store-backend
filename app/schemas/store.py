from pydantic import BaseModel
from datetime import datetime

class StoreBase(BaseModel):
    name: str
    description: str
    phone_number: str
    address: str


class CreateStore(StoreBase):
    pass


class StoreUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    phone_number: str | None = None
    address: str | None = None


class StoreResponse(StoreBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True
