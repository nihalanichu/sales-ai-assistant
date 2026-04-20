# This file will contain database connection and get_db function. we are using postgresql database.and 
# hostname: localhost, username: postgres, password: nichu, database name: shop_db

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:nichu@localhost:5432/shop_db")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BaseModel = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()