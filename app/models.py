from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Float
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone

order_product_association = Table(
    "asso_2",
    Base.metadata,
    Column("id_commandes", Integer, ForeignKey("Orders.id"), primary_key=True),
    Column("id_produit", Integer, ForeignKey("Products.id"), primary_key=True)
)


class CustomerDB(Base):
    __tablename__ = "Customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="user")
    firstname = Column(String(255), nullable=False, default="John")
    lastname = Column(String(255), nullable=False, default="Doe")
    street_number = Column(String(5), nullable=False, default="123")
    street = Column(String(255), nullable=False, default="SomeStreet")
    postalcode = Column(String(5), nullable=False, default="12345")
    city = Column(String(255), nullable=False, default="SomeCity")
    company_name = Column(String(255), nullable=False, default="SomeCompany")

    orders = relationship(
        "OrderDB",
        back_populates="customer",
        cascade="all, delete-orphan"
    )


class OrderDB(Base):
    __tablename__ = "Orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("Customers.id"))  

    customer = relationship("CustomerDB", back_populates="orders")  
    products = relationship(
        "ProductDB",
        secondary=order_product_association,
        back_populates="orders"
    )


class ProductDB(Base):
    __tablename__ = "Products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    price = Column(Float)
    description = Column(String)
    color = Column(String)
    stock = Column(Integer)

    orders = relationship(
        "OrderDB",
        secondary=order_product_association,
        back_populates="products"
    )
