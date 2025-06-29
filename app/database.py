"""
Database configuration module.

This module initializes the connection to the SQLite database using SQLAlchemy,
sets up the engine with the appropriate parameters,
and creates a local session factory (SessionLocal) for managing transactions.

It also defines the declarative base class (Base) for ORM model creation.
"""
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from logs.logger import setup_logger

APP_ENV = os.getenv("APP_ENV", "dev")

logger = setup_logger()

if APP_ENV == "prod":
    DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_PORT = os.getenv("DATABASE_PORT")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_URL = f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    DEFAULT_USERNAME = os.getenv("DEFAULT_USERNAME")
    DEFAULT_PASSWORD = os.getenv("DEFAULT_PASSWORD")
    connect_args = {}
elif APP_ENV == "dev":
    logger.critical("Application currently running in dev environnement. DON'T USE in production environnement")
    DATABASE_URL = "sqlite:///./items.db"
    connect_args = {"check_same_thread": False}
    DEFAULT_USERNAME = "TestUser"
    DEFAULT_PASSWORD = "TestPassword"
else:
    logger.critical("Not valable environnement found, please choose between dev or prod")

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Provide a database session generator.
    
    This function yields a new SQLAlchemy session for database operations
    and ensures that the session is properly closed after use,
    even if an exception occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()