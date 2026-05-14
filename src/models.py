from sqlalchemy import Column, Integer, String, Float
from .database import Base

class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    total_price = Column(Float)
    status = Column(String)