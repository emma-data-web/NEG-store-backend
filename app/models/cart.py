from sqlalchemy import Column, Integer, String, ForeignKey,  DateTime
from sqlalchemy.orm import relationship
from app.database.base import base
from datetime import datetime


class Cart(base):
  __tablename__ = "carts"

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey("users.id"), unique=True)
  created_at = Column(DateTime, default=datetime.utcnow)

  user = relationship("User", back_populates="cart")

  items = relationship("CartItem", back_populates="cart")