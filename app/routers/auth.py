from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.auth import UserCreate, UserCreateResponse, UserLogin, UserLoginResponse
from app.services.auth_services import create_user, login


auth_router = APIRouter()

@auth_router.post('/register', response_model=UserCreateResponse)
def regiter(user: UserCreate, db: Session = Depends(get_db)):
  return create_user(user=user, db=db)


@auth_router.post('/login', response_model=UserLoginResponse):
def signin(user: UserLogin, db: Session = Depends(get_db)):
  return login(user=user, db=db)


