from sqlalchemy.ext.asyncio import AsyncSession 
from app.schemas.product import ProductCreate, ProductUpdate
from app.models.user import User
from app.models.product import Product
from fastapi import HTTPException
import json
from app.utils.redis_client import client
from sqlalchemy import select

async def create_product(db: AsyncSession, data: ProductCreate, current_user: User):


  new_product = Product(
    name = data.name,
    price = data.price,
    description = data.description,
    category_id= data.category_id,
    image_url = data.image_url,
    store_id = current_user.store.id
     )
  
  db.add(new_product)
  await db.commit()
  await db.refresh(new_product)


  return new_product



async def get_product_by_id(db: AsyncSession, product_id: int):

  cache_key = f"product:{product_id}"

  cached_product =await  client.get(cache_key)

  
  if cached_product:
    return json.loads(cached_product)

  product = (await db.execute( select(Product).where(Product.id == product_id))).scalar_one_or_none()

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

  await client.setex(
    cache_key,           
    300,                
    json.dumps(product_data)  
)
  
  return product_data

