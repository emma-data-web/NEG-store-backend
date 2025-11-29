
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductUpdate
from app.models.user import User
from app.models.product import Product
from fastapi import HTTPException


def create_product(db: Session, data: ProductCreate, current_user: User):
  new_product = Product(
    name = data.name,
    price = data.price,
    description = data.description,
    category = data.category,
    image_url = data.image_url,
    owner_id = current_user.id
     )
  
  db.add(new_product)
  db.commit()
  db.refresh(new_product)

  return new_product



def get_product_by_id(db: Session, product_id: int):
  product = db.query(Product).filter(Product.id == product_id).first()

  if not product:
    raise HTTPException(status_code=404, detail="Product not found")
  
  return product

