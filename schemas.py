from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class OrderDetails(BaseModel):
    price: float
    description: str
    color: str


class Product(BaseModel):
    id: int
    createdAt: datetime
    name: str
    details: OrderDetails
    stock: int
    orderId: int

class ProductPost(BaseModel):
    createdAt: datetime
    name: str
    details: OrderDetails
    stock: int
    orderId: int


class Order(BaseModel):
    id: int
    createdAt: datetime
    customerId: int
    products: Optional[List[Product]] = []

class OrderPost(BaseModel):
    createdAt: datetime
    customerId: int
    products: Optional[List[Product]] = []

class Address(BaseModel):
    postalCode: str
    city: str


class Profile(BaseModel):
    firstName: str
    lastName: str


class Company(BaseModel):
    companyName: str


class Customer(BaseModel):
    id: int
    createdAt: datetime
    name: str
    username: str
    firstName: str
    lastName: str
    address: Address
    profile: Profile
    company: Company
    orders: Optional[List[Order]] = []

class CustomerPost(BaseModel):
    createdAt: datetime
    name: str
    username: str
    firstName: str
    lastName: str
    address: Address
    profile: Profile
    company: Company
    orders: Optional[List[Order]] = []