from sqlalchemy.orm import Session
from app.schemas.store import CreateStore, StoreUpdate
from app.models.user import User
from app.models.store import Store
from fastapi import HTTPException


def create_store(db: Session, data: CreateStore, current_user: User):
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



def update_store(db: Session, store_id: int, data: StoreUpdate, current_user: User):
    
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    
    if store.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this store")

    
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

    return store
