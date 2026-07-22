from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from app.database.base import base



class Category(base):
  __tablename__ = "categories"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String,unique=True, nullable=False, index=True)

  products = relationship("Product", back_populates="category")