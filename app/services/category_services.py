from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CreateCategory
from fastapi import HTTPException
from sqlalchemy import select


async def create_category(db: AsyncSession, category: CreateCategory, current: User):

  new_category = Category (
    name = category.name
  )

  if current.role != "admin":
    raise HTTPException(status_code=401, detail="not authorised")

  db.add(new_category)
  await db.commit()
  await db.refresh(new_category)


async def delete_category(db: AsyncSession, category_id: int, current: User):

  category = (await db.execute(select(Category).where(Category.id==category_id))).scalar_one_or_none()

  if not category:
    raise HTTPException(status_code=404, detail="category does not exist")
  
  if current.role != "admin":
    raise HTTPException(status_code=401, detail="not authorised")

  await db.delete(category)
  await db.commit()