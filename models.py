from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Float
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone

# Table d'association entre commandes et produits (Asso_2)
order_product_association = Table(
    "asso_2",
    Base.metadata,
    Column("id_commandes", Integer, ForeignKey("orders.id"), primary_key=True),
    Column("id_produit", Integer, ForeignKey("products.id"), primary_key=True)
)


class CustomerDB(Base):
    __tablename__ = "customers"  # Nom d'origine

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
   # created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    name = Column(String(255), nullable=False, default="")
    username = Column(String)
    first_name = Column(String(255), nullable=False, default="")
    last_name = Column(String(255), nullable=False, default="")
    postal_code = Column(String(255), nullable=False, default="")
    city = Column(String(255), nullable=False, default="")
    profile_first_name = Column(String(255), nullable=False, default="")
    profile_last_name = Column(String(255), nullable=False, default="")
    company_name = Column(String(255), nullable=False, default="")
    password = Column(String)

    orders = relationship(
        "OrderDB",
        back_populates="customer",
        cascade="all, delete-orphan"
    )


class OrderDB(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    customer_id = Column(Integer, ForeignKey("customers.id"))  

    customer = relationship("CustomerDB", back_populates="orders")  
    products = relationship(
        "ProductDB",
        secondary=order_product_association,
        back_populates="orders"
    )


class ProductDB(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    price = Column(Float)
    description = Column(String)
    color = Column(String)
    stock = Column(Integer)

    orders = relationship(
        "OrderDB",
        secondary=order_product_association,
        back_populates="products"
    )
