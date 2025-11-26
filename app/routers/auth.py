from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.auth import Message
from app.dependencies import get_db
from app.schemas.auth import UserCreate,  UserLogin, UserLoginResponse, ResetPassword, ForgotPassword
from app.services.auth_services import create_user, login, verify_user_email, send_reset_link, reset_user_password



auth_router = APIRouter()

@auth_router.post('/register', response_model=Message)
def regiter(user: UserCreate, db: Session = Depends(get_db)):
  

  create_user(user=user, db=db)

  return {"message": f"Account successfully created. A verification link has been sent to {user.email}."}

@auth_router.post('/login', response_model=UserLoginResponse)
def signin(user: UserLogin, db: Session = Depends(get_db)):
  return login(user=user, db=db)


@auth_router.get('/verify-email')
def verify_email(token: str, db: Session= Depends(get_db)):
  user = verify_user_email(token, db)
  return {'message', f'email for {user.first_name} is successful'}


@auth_router.post("/forgot-password", status_code=status.HTTP_200_OK)
def request_password_reset(request: ForgotPassword, db: Session = Depends(get_db)):
   
    return send_reset_link(db=db, email=request.email)

@auth_router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password_endpoint(data: ResetPassword, db: Session = Depends(get_db)):
   
    return reset_user_password(db=db, data=data)
  
