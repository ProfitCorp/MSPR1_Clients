from models import OrderDB, ProductDB
from sqlalchemy.orm import joinedload

def create_order(db, order_id, data):
    new_order = OrderDB(id=order_id, customer_id=data["customer_id"])
    db.add(new_order)

    if "products" in data:
        products = db.query(ProductDB).filter(ProductDB.id.in_(data["products"])).all()
        new_order.products = products

    db.commit()
    print(f"[✓] Commande {order_id} créée.")

def update_order(db, order_id, data):
    order = db.query(OrderDB).options(joinedload(OrderDB.products)).filter(OrderDB.id == order_id).first()
    if not order:
        print(f"[!] Commande {order_id} non trouvée pour mise à jour.")
        return

    if "customer_id" in data:
        order.customer_id = data["customer_id"]

    if "products" in data:
        products = db.query(ProductDB).filter(ProductDB.id.in_(data["products"])).all()
        order.products = products

    db.commit()
    print(f"[✓] Commande {order_id} mise à jour.")

def delete_order(db, order_id):
    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if not order:
        print(f"[!] Commande {order_id} non trouvée pour suppression.")
        return

    db.delete(order)
    db.commit()
    print(f"[✓] Commande {order_id} supprimée.")

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
    print(f"[✓] Produit {product_id} créé.")

def update_product(db, product_id, data):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product:
        print(f"[!] Produit {product_id} non trouvé pour mise à jour.")
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
    print(f"[✓] Produit {product_id} mis à jour.")

def delete_product(db, product_id):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product:
        print(f"[!] Produit {product_id} non trouvé pour suppression.")
        return

    db.delete(product)
    db.commit()
    print(f"[✓] Produit {product_id} supprimé.")        