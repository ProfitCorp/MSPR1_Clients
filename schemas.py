from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CustomersCreate(BaseModel):
    name: str
    price: float
    description: str
    color: str
    stock: str  # ou bool ou int selon le traitement
    order_id: Optional[int] = None  # optionnel si le produit est libre


class CustomersGet(CustomersCreate):
    id: int
    created_at: datetime
