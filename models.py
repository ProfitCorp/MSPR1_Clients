from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from database import Base
from datetime import datetime

class ItemDB(Base):
    __tablename__ = "Customers"
    
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(String)
    color = Column(String)
    stock = Column(Integer)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)


