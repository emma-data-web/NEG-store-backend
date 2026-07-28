from sqlalchemy.ext.asyncio import AsyncSession  
from app.schemas.store import CreateStore, StoreUpdate
from app.models.user import User
from app.models.store import Store
from fastapi import HTTPException
from app.utils.redis_client import client
import json
from sqlalchemy import select


async def create_store(db: AsyncSession, data: CreateStore, current_user: User):
    
    if current_user.role != "customer":
        raise HTTPException(status_code=401, detail="not authorised")

    new_store = Store(
        name = data.name,
        description = data.description,
        phone_number = data.phone_number,
        address = data.address,
        owner_id= current_user.id
    )

    db.add(new_store)
    await db.commit()
    await db.refresh(new_store)

    return new_store


async def get_store_by_id(db: AsyncSession, store_id: int):

    cached_key = f"store_id:{store_id}"

    cached_store = await client.get(cached_key)

    if cached_store:
        return json.loads(cached_store)

    store = (await db.execute(select(Store).where(Store.id == store_id))).scalar_one_or_none()


    if not store:
        raise HTTPException(status_code=404, detail="store not found")

    store_data = {
    "name": store.name,
    "description": store.description,
    "phone_number": store.phone_number,
    "address": store.address
    }

    await client.setex(
        cached_key,
        300,
        json.dumps(store_data)
    )

    return store_data





async def update_store(db: AsyncSession, store_id: int, data: StoreUpdate, current_user: User):
    
    store = (await db.execute(select(Store).where(Store.id == store_id))).scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    
    if current_user.role != "seller":
        raise HTTPException(status_code=401, detail="not authorised")

    
    if data.name is not None:
        store.name = data.name

    if data.description is not None:
        store.description = data.description

    if data.phone_number is not None:
        store.phone_number = data.phone_number

    if data.address is not None:
        store.address = data.address

    
    await db.commit()
    await db.refresh(store)

    cached_key = f"store_id:{store_id}"

    await client.delete(cached_key)


    return store


async def delete_store(db: AsyncSession, store_id: int, current_user: User):
    store =( await db.execute(select(Store).where(Store.id==store_id))).scalar_one_or_none()

    if not store:
        raise HTTPException(status_code=404, detail="store does not exist")
    
    if store.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="not authorised for this action")
    
    await db.delete(store)
    await db.commit()

    cached_key = f"store_id:{store_id}"

    await client.delete(cached_key)

    return {"message":"store deleted"}

