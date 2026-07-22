from sqlalchemy.orm import Session
from app.schemas.user import UserInfoResponse
from app.models.user import User
from app.services.user_services import user_profile, delete_user
from fastapi import HTTPException, APIRouter, Depends
from app.dependencies import get_db
from app.services.user_services import get_current_user


user_router = APIRouter()


@user_router.get('/user-profile/{user_id}', response_model=UserInfoResponse)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):

  profile = user_profile(db=db, user_id=user_id)

  return profile


@user_router.delete("/delete-user/{user_id}")
def delete_user(user_id: int, db: Session= Depends(get_db), current_user: User = Depends(get_current_user)):

  delete_user(user_id=user_id,db=db,current_user=current_user)