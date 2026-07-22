from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartItemCreate


def add_to_cart(db: Session, data: CartItemCreate, current_user: User):

    
    cart = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).first()

    
    if not cart:
        cart = Cart(
            user_id=current_user.id
        )
        db.add(cart)
        db.commit()
        db.refresh(cart)

    
    product = db.query(Product).filter(
        Product.id == data.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == data.product_id
    ).first()

    if cart_item:
        cart_item.quantity += data.quantity
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=data.product_id,
            quantity=data.quantity
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)

    return cart_item



def get_user_cart(db: Session, current_user: User):

    cart = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).first()

    if not cart:
        return None

    return cart


def update_cart_item(
    db: Session,
    cart_item_id: int,
    quantity: int,
    current_user: User
):

    cart_item = db.query(CartItem).join(Cart).filter(
        CartItem.id == cart_item_id,
        Cart.user_id == current_user.id
    ).first()


    if not cart_item:
        return None


    cart_item.quantity = quantity

    db.commit()
    db.refresh(cart_item)

    return cart_item


def remove_cart_item(
    db: Session,
    cart_item_id: int,
    current_user: User
):

    cart_item = db.query(CartItem).join(Cart).filter(
        CartItem.id == cart_item_id,
        Cart.user_id == current_user.id
    ).first()


    if not cart_item:
        return None


    db.delete(cart_item)
    db.commit()

    return True