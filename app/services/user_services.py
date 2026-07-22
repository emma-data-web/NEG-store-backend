from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from  app.core.security import bearer_scheme
from fastapi.security import HTTPAuthorizationCredentials
from app.dependencies import get_db
from app.core.config import Settings
from jose import jwt, JWTError
from app.models.user import User
from app.schemas.user import UserInfoResponse



def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session= Depends(get_db)):
    token = credentials.credentials
    try:
        
        payload = jwt.decode(
            token, 
            Settings.SECRET_KEY, 
            algorithms=[Settings.JWT_ALGORITHM]
        )

        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    
    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User no longer exists",
        )

    return user




def get_current_admin(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only"
        )

    return current_user



def get_current_seller(
    current_user: User = Depends(get_current_user)
):
  
    if current_user.role != "seller":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sellers only"
        )

    return current_user




def user_profile(db: Session, user_id:int):
    user = db.query(User).filter(User.id == user_id)

    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    return user


def delete_user(db:Session, user_id:int, current_user: User):
    user = db.query(User).filter(User.id == user_id).first()

    if not user: 
        raise HTTPException(status_code=404, details="user does not exist")
    
    if user_id!= current_user.id:
        raise HTTPException(status_code=403, detail="not authorised to delete this account")
    
    db.delete(user)
    db.commit()

    return {"message": "user deleted"}