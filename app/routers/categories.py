from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import User
from app.schemas.category import CreateCategory
from app.services.user_services import get_current_admin
from app.services.category_services import create_category, delete_category


category_router = APIRouter()

@category_router.post("/create-category")
def create_categories(category: CreateCategory, db: Session = Depends(get_db), current: User = Depends(get_current_admin)):

  create_category(db=db, category=category,current=current)

  return {"message":"category creaated"}


@category_router.delete("/delete-category/{category_id}")
def delete_categories(category_id: int, db: Session = Depends(get_db), current: User = Depends(get_current_admin)):
  delete_category(db=db, category_id=category_id,current=current)

  return {"message":"deleted successfully"}