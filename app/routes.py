from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controllers import get_all_customers, create_customer, delete_customer, update_customer
from database import get_db
from schemas import Customer, CustomerPost, LoginInput
from fastapi import HTTPException
from auth.auth import create_access_token, authenticate_user
from auth.security import JWTBearer

router = APIRouter()


@router.get("/customers/",dependencies=[Depends(JWTBearer())], response_model=list[Customer])
def get_customers(db: Session = Depends(get_db)):
    return get_all_customers(db)


@router.post("/customers/",dependencies=[Depends(JWTBearer())], response_model=Customer)
def add_customer(customer: CustomerPost, db: Session = Depends(get_db)):
    return create_customer(db, customer)


@router.put("/customers/{customer_id}",dependencies=[Depends(JWTBearer())], response_model=Customer)
def modify_customer(
    customer_id: str, customer: CustomerPost, db: Session = Depends(get_db)
):
    updated = update_customer(db, customer_id, customer)
    if not updated:
        return {"error": "Client non trouvé"}
    return updated


@router.delete("/customers/{customer_id}",dependencies=[Depends(JWTBearer())])
def remove_customer(customer_id: str, db: Session = Depends(get_db)):
    deleted = delete_customer(db, customer_id)
    if not deleted:
        return {"error": "Client non trouvé"}
    return {"message": f"Client {customer_id} supprimé"}

@router.post("/token")
def login_user(user: LoginInput):
    
    if not authenticate_user(user.username, user.password):
        raise HTTPException(status_code=401, detail=user.password)

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}