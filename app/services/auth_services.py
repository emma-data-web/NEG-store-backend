from app.core.security import hash_password,verify_password, create_access_token, decode_access_token
from app.schemas.auth import UserCreate, UserLogin
from sqlalchemy.orm import Session
from fastapi import HTTPException, Query
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
    hashed_password = harsed_pwd,
    is_verified = False

    )

  db.add(new_user)
  db.commit()

 

  return new_user



def login(user: UserLogin, db: Session):
  db_user = db.query(User).filter(User.email == user.email).first()
  if not db_user or not verify_password(user.password, db_user.hashed_password):
    raise HTTPException(status_code=401, detail='invalid username or password')
  access_token = create_access_token({"sub": str(db_user.id)})
  return {"access_token": access_token, "token_type": "bearer"}

def generate_verification_link(user: User):
    token = create_access_token({"sub": str(user.id)})
    link = f"http://localhost:8000/auth/verify-email?token={token}"
    return link


def verify_user_email(token: str, db: Session):
    payload = decode_access_token(token)
    user_id = int(payload.get("sub"))

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_verified = True
    db.commit()

    return user