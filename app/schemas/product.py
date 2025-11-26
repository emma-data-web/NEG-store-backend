from pydantic import BaseModel, EmailStr

class CreateProduct(BaseModel):
  name: str
  brand: str
  price: int
  tags: str
  