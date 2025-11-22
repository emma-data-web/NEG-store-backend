from app.core.config import Settings
from app.core.security import hash_password,verify_password, create_access_token, decode_access_token
from app.schemas.auth import UserCreate, UserCreateResponse, UserLogin, UserLoginResponse
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User


def create_user(user:UserCreate, db:Session):
  existing_user = db.query(User).filter(User.email== user.email).first()

  if existing_user:
    raise HTTPException(status_code=400, detail='User already exist')