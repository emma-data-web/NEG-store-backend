from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from app.database.base import base
from datetime import datetime

class Store(base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    Description= Column(String, nullable=False)
    phone_number = Column(String,nullable=False),
    address = Column(String,  nullable= False)
    owner_id = Column(Integer, ForeignKey("users.id")) 
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="store")