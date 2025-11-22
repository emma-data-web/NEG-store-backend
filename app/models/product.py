from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.database.base import base

class Product(base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))  

    owner = relationship("User", back_populates="products")
