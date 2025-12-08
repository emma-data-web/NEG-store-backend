from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from  app.core.security import bearer_scheme
from fastapi.security import HTTPAuthorizationCredentials
from app.dependencies import get_db
from app.core.config import Settings
from jose import jwt, JWTError
from app.models.user import User



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
