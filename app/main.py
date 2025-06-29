from fastapi import FastAPI
from database import Base, engine
import routes
from init import init_admin_user
from threading import Thread
from mq.receive import receive_order_message, receive_product_message
from logs.logger import setup_logger

Base.metadata.create_all(bind=engine)

logger = setup_logger()

app = FastAPI()

app.include_router(routes.router)

init_admin_user()

@app.on_event("startup")
def _start_listener():
    """Launch the RabbitMQ listener in a background thread."""
    Thread(target=receive_order_message, daemon=True).start()
    Thread(target=receive_product_message, daemon=True).start()
    logger.info("Application start")
    