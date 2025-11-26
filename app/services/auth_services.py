from app.core.security import hash_password,verify_password, create_access_token, decode_access_token
from app.schemas.auth import UserCreate, UserLogin, ResetPassword
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.core.email import send_verification_email
from app.core.security import reset_password_access_token
from app.core.email import send_reset_password_email
from jose import jwt, JWTError
from app.core.config import Settings
from fastapi import status


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
    db.refresh(new_user)
    
    verification_link = generate_verification_link(new_user)
    send_verification_email(new_user.email, verification_link)

    return new_user



def login(user: UserLogin, db: Session):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail='invalid username or password')
    if not db_user.is_verified:
        raise HTTPException(
            status_code=403, 
            detail='Account not verified. Please check your email for the verification link.'
        )
    access_token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

def generate_verification_link(user: User):
    
    token = create_access_token({"sub": str(user.id)})
    link = f"http://localhost:8000/api/v1/auth/verify-email?token={token}"
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

    
def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def send_reset_link(db: Session, email: str):
    
    db_user = get_user_by_email(db, email)
    
    if not db_user:
        
        return {"message": "If a user with that email exists, a password reset link has been sent."}

   
    reset_token_claims = {
        "sub": str(db_user.id),
        "scope": "password_reset"
    }
    reset_token = reset_password_access_token(reset_token_claims)
    
    
    reset_link = f"http://localhost:8000/api/v1/auth/reset-password?token={reset_token}"
    
    
    send_reset_password_email(db_user.email, reset_link)
    
    return {"message": "If a user with that email exists, a password reset link has been sent."}


def reset_user_password(db: Session, data: ResetPassword):
    try:
        
        payload = jwt.decode(data.token, Settings.SECRET_KEY, algorithms=[Settings.JWT_ALGORITHM])
        user_id = payload.get("sub")
        scope = payload.get("scope")
        
        
        if scope != "password_reset":
            raise JWTError("Invalid token scope.")
            
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid or expired password reset token."
        )

    db_user = db.query(User).filter(User.id == int(user_id)).first()
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found."
        )

    
    db_user.hashed_password = hash_password(data.new_password)
    db.commit()
    
    return {"message": "Password successfully reset. You can now log in with your new password."}