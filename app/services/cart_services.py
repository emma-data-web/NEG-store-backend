from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartItemCreate

async def add_to_cart(
    db: AsyncSession,
    data: CartItemCreate,
    current_user: User
):

    try:
        
        stmt = select(Cart).where(
            Cart.user_id == current_user.id
        )

        result = await db.execute(stmt)

        cart = result.scalar_one_or_none()


        
        if not cart:
            cart = Cart(
                user_id=current_user.id
            )

            db.add(cart)

            
            await db.flush()


        
        stmt = select(Product).where(
            Product.id == data.product_id
        )

        result = await db.execute(stmt)

        product = result.scalar_one_or_none()


        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )


        
        stmt = select(CartItem).where(
            CartItem.cart_id == cart.id,
            CartItem.product_id == data.product_id
        )

        result = await db.execute(stmt)

        cart_item = result.scalar_one_or_none()


        
        if cart_item:
            cart_item.quantity += data.quantity

        
        else:
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=data.product_id,
                quantity=data.quantity
            )

            db.add(cart_item)


        
        await db.commit()

        await db.refresh(cart_item)

        return cart_item


    except Exception:
        
        await db.rollback()
        raise



async def get_user_cart(db: AsyncSession, current_user: User):

    cart = (await db.execute(select(Cart).where(
        Cart.user_id == current_user.id
    ))).scalar_one_or_none()

    if not cart:
        return None

    return cart


async def update_cart_item(
    db: AsyncSession,
    cart_item_id: int,
    quantity: int,
    current_user: User
):

    cart_item = (await db.execute(select(CartItem).join(Cart).where(
        CartItem.id == cart_item_id,
        Cart.user_id == current_user.id
    ))).scalar_one_or_none()


    if not cart_item:
        return None


    cart_item.quantity = quantity

    await db.commit()
    await db.refresh(cart_item)

    return cart_item


async def remove_cart_item(
    db: AsyncSession,
    cart_item_id: int,
    current_user: User
):

    cart_item = (await db.execute(select(CartItem).join(Cart).where(
        CartItem.id == cart_item_id,
        Cart.user_id == current_user.id
    ))).scalar_one_or_none()


    if not cart_item:
        return None


    await db.delete(cart_item)
    await db.commit()

    return True