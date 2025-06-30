from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers import get_all_customers, create_customer, delete_customer, update_customer
from database import get_db
from schemas import Customer, CustomerPost, LoginInput
from fastapi import HTTPException
from auth.auth import create_access_token, authenticate_user
from auth.security import JWTBearer
from logs.logger import setup_logger

router = APIRouter()

logger = setup_logger()

@router.get("/customers/",dependencies=[Depends(JWTBearer())], response_model=list[Customer])
def get_customers(token_data: dict = Depends(JWTBearer()), db: Session = Depends(get_db)):
    role = token_data.get("role")
    user_id = token_data.get("user_id")
    logger.info("GET /customers")
    logger.debug(role)
    logger.debug(user_id)
    return get_all_customers(db, user_id, role)


@router.post("/customers/",dependencies=[Depends(JWTBearer())], response_model=Customer)
def add_customer(customer: CustomerPost, db: Session = Depends(get_db)):
    logger.info("POST /customers")
    logger.debug(customer)
    return create_customer(db, customer)


@router.put("/customers/{customer_id}",dependencies=[Depends(JWTBearer())], response_model=Customer)
def modify_customer(customer_id: str, customer: CustomerPost, db: Session = Depends(get_db), token_data: dict = Depends(JWTBearer())):
    role = token_data.get("role")
    user_id = token_data.get("user_id")
    if role != "admin" and user_id != int(customer_id):
        raise HTTPException(status_code=403, detail="Not authorized to modify this customer")
    
    updated = update_customer(db, customer_id, customer)
    if not updated:
        raise HTTPException(status_code=404, detail="Customer not found")
    logger.info("PUT /customers")
    logger.debug(role)
    logger.debug(user_id)
    logger.debug(updated)
    return updated


@router.delete("/customers/{customer_id}",dependencies=[Depends(JWTBearer())])
def remove_customer(customer_id: str, db: Session = Depends(get_db), token_data: dict = Depends(JWTBearer())):
    role = token_data.get("role")
    user_id = token_data.get("user_id")
    if role != "admin" and user_id != int(customer_id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    
    deleted = delete_customer(db, customer_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Customer not found")
    logger.info("DEL /customers")
    logger.debug(role)
    logger.debug(user_id)
    return 200

@router.post("/token")
def login_user(user: LoginInput):
    db_user = authenticate_user(user.username, user.password)
    if not db_user:
        logger.debug("Invalid credentials to request token")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = token = create_access_token({
        "sub": db_user.username,
        "role": db_user.role,
        "user_id": db_user.id
    })
    logger.info("Token requested")
    logger.debug(f"Token requested for {db_user.id} with {db_user.role} role")
    return {"access_token": token, "token_type": "bearer"}