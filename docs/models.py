# this will contain user model with fields fullname, email, password
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from docs.database import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

    chathistory = relationship("ChatHistory", back_populates="user")

# create product table with id, title, category, price, description, current_stock, created_at
class Product(BaseModel):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    category = Column(String, index=True)
    price = Column(Integer)
    description = Column(String)
    current_stock = Column(Integer)
    created_at = Column(DateTime, default=DateTime.utcnow())

# create chathistory table with id - int, user_id - int, sender - string, message - string, timestamp - DateTime
class ChatHistory(BaseModel):
    __tablename__ = 'chathistory'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    sender = Column(String, index=True)
    message = Column(String)
    timestamp = Column(DateTime, default=DateTime.utcnow())

    user = relationship("User", back_populates="chathistory")