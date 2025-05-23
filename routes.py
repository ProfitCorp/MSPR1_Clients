from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers import get_all_customers, create_customer, delete_customer
from database import get_db
from schemas import Customer

router = APIRouter()

@router.get("/customers/", response_model=list[Customer])
def get_customers(db: Session = Depends(get_db)):
    return get_all_customers(db)

@router.post("/customers/", response_model=Customer)
def add_customer(customer: Customer, db: Session = Depends(get_db)):
    return create_customer(db, customer)

@router.put("/customers/{customer_id}", response_model=Customer)
def modify_customer(customer_id: str, customer: Customer, db: Session = Depends(get_db)):
    updated = update_customer(db, customer_id, customer)
    if not updated:
        return {"error": "Client non trouvé"}
    return updated

@router.delete("/customers/{customer_id}")
def remove_customer(customer_id: str, db: Session = Depends(get_db)):
    deleted = delete_customer(db, customer_id)
    if not deleted:
        return {"error": "Client non trouvé"}
    return {"message": f"Client {customer_id} supprimé"}
