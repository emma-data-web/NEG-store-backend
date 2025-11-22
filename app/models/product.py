from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from app.database.base import base
from datetime import datetime

class Product(base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))  
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="Product")
