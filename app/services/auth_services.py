from app.core.security import hash_password,verify_password, create_access_token, decode_access_token
from app.schemas.auth import UserCreate, UserLogin
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User


def create_user(user:UserCreate, db:Session):
  existing_user = db.query(User).filter(User.email== user.email).first()

  if existing_user:
    raise HTTPException(status_code=400, detail='User already exist')
  
  harsed_pwd = hash_password(user.password)

  new_user = User(
    first_name = user.first_name,
    last_name = user.last_name,
    username = user.username,
    email = user.email,
    hashed_password = harsed_pwd
  )

  db.add(new_user)
  db.commit()

  return new_user



def login(user: UserLogin, db: Session):
  db_user = db.query(User).filter(User.email == user.email).first()
  if not db_user or verify_password(user.password, db_user.hashed_password):
    raise HTTPException(status_code=401, detail='invalid username or password')
  access_token = create_access_token({"sub": str(db_user.id)})
  return {"access_token": access_token, "token_type": "bearer"}