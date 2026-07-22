from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import User
from app.schemas.cart import CartItemCreate,CartItemResponse
from app.services.user_services import get_current_user
from app.services.cart_services import add_to_cart, get_user_cart,update_cart_item, remove_cart_item


cart_router = APIRouter()

@cart_router.post("/add-to-cart",response_model=CartItemResponse)
def create_add_to_cart(data: CartItemCreate, db: Session = Depends(get_db), current_user: User =Depends(get_current_user)):

  cart_item = add_to_cart(db=db,data=data, current_user=current_user)

  return cart_item


@cart_router.get("/my-cart")
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    cart = get_user_cart(
        db=db,
        current_user=current_user
    )

    return cart



@cart_router.patch("/cart-item/{cart_item_id}")
def update_item(
    cart_item_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return update_cart_item(
        db=db,
        cart_item_id=cart_item_id,
        quantity=quantity,
        current_user=current_user
    )



@cart_router.delete("/cart-item/{cart_item_id}")
def remove_item(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return remove_cart_item(
        db=db,
        cart_item_id=cart_item_id,
        current_user=current_user
    )