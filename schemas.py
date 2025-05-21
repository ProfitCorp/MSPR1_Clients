from pydantic import BaseModel
from datetime import datetime

class Details(BaseModel):
    price: float
    description: str
    color: str

class Products(BaseModel):
    name: str
    details: Details
    stock: int

class ProductsGet(BaseModel):
    name: str
    details: Details
    stock: int
    id: int