#app/models/user_model.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    role = Column(String, default="user")
    cart_items = relationship("CartItem", back_populates="user")
    orders = relationship("app.models.order_model.Order", back_populates="user")