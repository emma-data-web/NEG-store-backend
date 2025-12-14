from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import User
from app.services.product_services import create_product, get_product_by_id
from app.schemas.product import ProductCreate, ProductResponse
from app.services.user_services import get_current_user


product_router = APIRouter()

@product_router.post('/create-product', response_model=ProductResponse)
def product_create(data: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

  new_product = create_product(db=db,data= data, current_user=current_user)

  return new_product


@product_router.get('/get-product-by-id/{product_id}')
def get_product(product_id:int , db: Session = Depends(get_db)):

  get_prod = get_product_by_id(db=db, product_id=product_id)

  return get_prod