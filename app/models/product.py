from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from app.database.base import base
from datetime import datetime

class Product(base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    description = Column(String, nullable=False)
    quantity = Column(Integer, default=0)
    image_url = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    store_id = Column(Integer, ForeignKey("users.id")) 
    category = Column(String, index=True) 
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("Store", back_populates="owner")
