"""
This module generate an JWT for API Authentication
"""
from fastapi import Request, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta
from database import SessionLocal
from models import CustomerDB
import os
import bcrypt
from logs.logger import setup_logger

logger = setup_logger()

APP_ENV = os.getenv("APP_ENV", "dev")
db = SessionLocal()

if APP_ENV == "prod":
    SECRET_KEY = os.getenv("SECRET_KEY")
else:
    SECRET_KEY = "ExampleSecretKey"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.debug(token)
    return token

def authenticate_user(username: str, password: str, db=db):
    user = db.query(CustomerDB).where(CustomerDB.username == username).first()
    logger.debug(user)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    logger.info("User authenticated")
    return user

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))