from fastapi import FastAPI
from database import Base, engine
import routes
from init import init_admin_user
from threading import Thread

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routes.router)

init_admin_user()

@app.on_event("startup")
def _start_listener():
    """Launch the RabbitMQ listener in a background thread."""
    Thread(target=listen_for_user_messages, daemon=True).start()