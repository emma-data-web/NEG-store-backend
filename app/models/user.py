from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database.base import base
from datetime import datetime

class User(base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True, index=True)
  first_name = Column(String)
  last_name = Column(String)
  email = Column(String, unique=True, index=True)
  hashed_password = Column(String)
  is_active = Column(Boolean, default=True)
  created_at = Column(DateTime, default=datetime.utcnow)