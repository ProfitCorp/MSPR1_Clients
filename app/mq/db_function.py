from models import OrderDB, ProductDB
from sqlalchemy.orm import joinedload

def create_order(db, order_id, data):
    new_order = OrderDB(id=order_id, customer_id=data["customer_id"])
    db.add(new_order)

    if "products" in data:
        products = db.query(ProductDB).filter(ProductDB.id.in_(data["products"])).all()
        new_order.products = products

    db.commit()

def update_order(db, order_id, data):
    order = db.query(OrderDB).options(joinedload(OrderDB.products)).filter(OrderDB.id == order_id).first()
    if not order:
        return

    if "customer_id" in data:
        order.customer_id = data["customer_id"]

    if "products" in data:
        products = db.query(ProductDB).filter(ProductDB.id.in_(data["products"])).all()
        order.products = products

    db.commit()

def delete_order(db, order_id):
    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if not order:
        return

    db.delete(order)
    db.commit()

def create_product(db, product_id, data):
    new_product = ProductDB(
        id=product_id,
        name=data.get("name"),
        price=data["details"].get("price"),
        description=data["details"].get("description"),
        color=data["details"].get("color"),
        stock=data.get("stock")
    )
    db.add(new_product)
    db.commit()

def update_product(db, product_id, data):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product:
        return

    if "name" in data:
        product.name = data["name"]
    if "details" in data:
        details = data["details"]
        if "price" in details:
            product.price = details["price"]
        if "description" in details:
            product.description = details["description"]
        if "color" in details:
            product.color = details["color"]
    if "stock" in data:
        product.stock = data["stock"]

    db.commit()

def delete_product(db, product_id):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product:
        return

    db.delete(product)
    db.commit()