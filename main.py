from fastapi import FastAPI
from database import Base, engine
import routes

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routes.router)
