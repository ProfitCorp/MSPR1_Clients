from fastapi import FastAPI
from database import Base, engine
import routes
from init import init_admin_user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routes.router)

init_admin_user()