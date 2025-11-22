from pydantic import BaseModel, EmailStr

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