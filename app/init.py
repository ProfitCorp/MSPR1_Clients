import logging
from auth.security import hash_password
from database import SessionLocal, DEFAULT_USERNAME, DEFAULT_PASSWORD
from models import CustomerDB

if (DEFAULT_USERNAME == None or DEFAULT_PASSWORD == None):
    raise EnvironmentError("DEFAULT_USERNAME or DEFAULT_PASSWORD not variable defined")

logger = logging.getLogger("uvicorn")

def init_admin_user():
    db = SessionLocal()
    try:
        user_count = db.query(CustomerDB).count()
        if user_count == 0:
            admin = CustomerDB(
                username=DEFAULT_USERNAME,
                password=hash_password(DEFAULT_PASSWORD)
                role="admin"
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()
