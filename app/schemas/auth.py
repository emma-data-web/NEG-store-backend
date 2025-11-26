from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
  first_name : str
  last_name : str
  username : str
  email : EmailStr
  password : str


class UserCreateResponse(BaseModel):
  id: int
  username: str
  email: EmailStr

  class Config:
    orm_mode = True


class UserLogin(BaseModel):
  email : EmailStr
  password : str


class UserLoginResponse(BaseModel):
  access_token: str
  token_type: str = "bearer"


class Message(BaseModel):
   message: str

class ForgotPassword(BaseModel):
  email: EmailStr
  
class ResetPassword(BaseModel):
    """Schema for submitting a new password with the reset token."""
    token: str
    new_password: str = Field(min_length=8)