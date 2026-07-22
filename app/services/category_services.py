from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CreateCategory
from fastapi import HTTPException


def create_category(db: Session, category: CreateCategory, current: User):

  new_category = Category (
    name = category.name
  )

  if current.role != "admin":
    raise HTTPException(status_code=401, detail="not authorised")

  db.add(new_category)
  db.commit()
  db.refresh(new_category)


def delete_category(db: Session, category_id: int, current: User):

  category =db.query(Category).filter(Category.id==category_id).first()

  if not category:
    raise HTTPException(status_code=404, detail="category does not exist")
  
  if current.role != "admin":
    raise HTTPException(status_code=401, detail="not authorised")

  db.delete(category)
  db.commit()