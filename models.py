from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
from datetime import timezone


class CustomerDB(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    name = Column(String)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    postal_code = Column(String)
    city = Column(String)
    profile_first_name = Column(String)
    profile_last_name = Column(String)
    company_name = Column(String)

    orders = relationship(
        "OrderDB",
        back_populates="customer",
        cascade="all, delete-orphan"  # <- C'est ça qui va supprimer les commandes liées automatiquement
    )


class OrderDB(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    customer_id = Column(String, ForeignKey("customers.id"))

    customer = relationship("CustomerDB", back_populates="orders")
    products = relationship(
        "ProductDB",
        back_populates="order",
        cascade="all, delete-orphan"  # <- ça supprime aussi automatiquement les produits liés
    )


class ProductDB(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    price = Column(String)  # Format "97,00"
    description = Column(String)
    color = Column(String)
    stock = Column(String)  # "rupture", etc.
    order_id = Column(String, ForeignKey("orders.id"))

    order = relationship("OrderDB", back_populates="products")
