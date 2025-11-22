from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.core.config import Settings 


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)




def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        
        expire = datetime.utcnow() + timedelta(minutes=Settings.ACESS_TOKEN_EXPIRE_MINUTE)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        Settings.SECRET_KEY, 
        algorithm=Settings.JWT_ALGORITHM
    )
    return encoded_jwt




def decode_access_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        
        payload = jwt.decode(
            token, 
            Settings.SECRET_KEY, 
            algorithms=[Settings.JWT_ALGORITHM]
        )
        
        user_id: str = payload.get("sub") 
        if user_id is None:
            raise credentials_exception
        
        
        return user_id 
        
    except JWTError:
        raise credentials_exception