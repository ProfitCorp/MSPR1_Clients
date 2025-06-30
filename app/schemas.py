from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class OrderDetails(BaseModel):
    price: float
    description: str
    color: str


class Product(BaseModel):
    id: int
    name: str
    details: OrderDetails
    stock: int

class ProductPost(BaseModel):
    name: str
    details: OrderDetails
    stock: int


class Order(BaseModel):
    id: int
    customerId: int
    products: Optional[List[Product]] = []

class OrderPost(BaseModel):
    customerId: int
    products: Optional[List[Product]] = []

class Address(BaseModel):
    streetNumber: str
    street: str
    postalCode: str
    city: str

class Customer(BaseModel):
    id: int
    username: str
    password: str
    firstName: str
    lastName: str
    address: Address
    companyName: str
    orders: Optional[List[Order]] = []

class CustomerPost(BaseModel):
    username: str
    password: str
    firstName: str
    lastName: str
    address: Address
    companyName: str
    orders: Optional[List[Order]] = []

class LoginInput(BaseModel):
    username: str
    password: str