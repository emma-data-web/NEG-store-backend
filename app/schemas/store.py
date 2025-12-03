from pydantic import BaseModel
from datetime import datetime


class StoreBase(BaseModel):
  id: int
  name: str
  description: str
  phone_number: int
  address: str


class Createstore(StoreBase):
  created_at: datetime


class StoreUpdate(StoreBase):
  phone_number: int  | None = None
  address: str | None = None


class StoreResponse(StoreBase):
  owner_id : int

  class Config:
    orm_mode = True