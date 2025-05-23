from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class OrderDetails(BaseModel):
    price: str 
    description: str
    color: str


class Product(BaseModel):
    createdAt: datetime
    name: str
    details: OrderDetails
    stock: str
    id: str
    orderId: str


class Order(BaseModel):
    createdAt: datetime
    id: str
    customerId: str
    products: Optional[List[Product]] = None  # Certains orders n'ont pas de produits


class Address(BaseModel):
    postalCode: str
    city: str


class Profile(BaseModel):
    firstName: str
    lastName: str


class Company(BaseModel):
    companyName: str


class Customer(BaseModel):
    createdAt: datetime
    name: str
    username: str
    firstName: str
    lastName: str
    address: Address
    profile: Profile
    company: Company
    id: str
    orders: List[Order]
