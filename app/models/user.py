from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database.base import base
from datetime import datetime

class User(base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True, index=True)
  first_name = Column(String)
  last_name = Column(String)
  username = Column(String, unique=True)
  email = Column(String, unique=True, index=True)
  hashed_password = Column(String)
  is_active = Column(Boolean, default=True)
  is_verified = Column(Boolean,default=False),
  created_at = Column(DateTime, default=datetime.utcnow)


  products = relationship("Product", back_populates="owner")