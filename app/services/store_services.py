from sqlalchemy.orm import Session
from app.schemas.store import CreateStore, StoreUpdate
from app.models.user import User
from app.models.store import Store
from fastapi import HTTPException
from app.utils.redis_client import client
import json


def create_store(db: Session, data: CreateStore, current_user: User):
    
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
    db.commit()
    db.refresh(new_store)

    return new_store


def get_store_by_id(db: Session, store_id: int):

    cached_key = f"store_id:{store_id}"

    cached_store = client.get(cached_key)

    if cached_store:
        return json.loads(cached_store)

    store = db.query(Store).filter(Store.id == store_id).first()


    if not store:
        raise HTTPException(status_code=404, detail="store not found")

    store_data = {
    "name": store.name,
    "description": store.description,
    "phone_number": store.phone_number,
    "address": store.address
    }

    client.setex(
        cached_key,
        300,
        json.dump(store_data)
    )

    return store_data





def update_store(db: Session, store_id: int, data: StoreUpdate, current_user: User):
    
    store = db.query(Store).filter(Store.id == store_id).first()
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

    
    db.commit()
    db.refresh(store)

    cached_key = f"store_id:{store_id}"

    client.delete(cached_key)


    return store


def delete_store(db: Session, store_id: int, current_user: User):
    store = db.query(Store).filter(Store.id==store_id).first()

    if not store:
        raise HTTPException(status_code=404, detail="store does not exist")
    
    if store.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="not authorised for this action")
    
    db.delete(store)
    db.commit()

    cached_key = f"store_id:{store_id}"

    client.delete(cached_key)

    return {"message":"store deleted"}

