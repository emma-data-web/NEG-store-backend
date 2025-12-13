from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.store import StoreResponse, CreateStore, StoreUpdate
from app.services.store_services import create_store, update_store
from app.services.user_services import get_current_user
from app.models.user import User

store_router = APIRouter()

@store_router.post('/create-store', response_model=StoreResponse)
def store(data : CreateStore,
  db: Session = Depends(get_db), 
           current_user: User = Depends(get_current_user)):

  new_store =create_store(db=db, data=data, current_user =current_user)

  return new_store



@store_router.put('/update-store/{store_id}')
def store_update(
    store_id: int,
    data: StoreUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_store = update_store(db, store_id, data, current_user)
    return updated_store
