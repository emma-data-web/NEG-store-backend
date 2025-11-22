from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserInfoResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    created_at: datetime

    class Config:
      orm_mode = True


class UpdateUsername(BaseModel):
    username: str
