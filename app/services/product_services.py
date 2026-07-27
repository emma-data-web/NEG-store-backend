
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductUpdate
from app.models.user import User
from app.models.product import Product
from fastapi import HTTPException
import json
from app.utils.redis_client import client


def create_product(db: Session, data: ProductCreate, current_user: User):


  new_product = Product(
    name = data.name,
    price = data.price,
    description = data.description,
    category_id= data.category_id,
    image_url = data.image_url,
    store_id = current_user.store.id
     )
  
  db.add(new_product)
  db.commit()
  db.refresh(new_product)


  return new_product



def get_product_by_id(db: Session, product_id: int):

  cache_key = f"product:{product_id}"

  cached_product = client.get(cache_key)

  
  if cached_product:
    return json.loads(cached_product)

  product = db.query(Product).filter(Product.id == product_id).first()

  if not product:
    raise HTTPException(status_code=404, detail="Product not found")

  product_data = {
    "name": product.name,
    "price": float(product.price),
    "description": product.description,
    "quantity": product.quantity,
    "category_id": product.category_id,
    "image_url": product.image_url
  }

  client.setex(
    cache_key,           
    300,                
    json.dumps(product_data)  
)
  
  return product_data

