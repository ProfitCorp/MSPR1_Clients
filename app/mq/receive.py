import pika
import json
from database import SessionLocal
from mq.db_function import create_order, update_order, delete_order, create_product, update_product, delete_product

def receive_order_message():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    channel.exchange_declare(exchange="orders.sync", exchange_type="fanout")
    channel.queue_declare(queue="api_users_orders", durable=True)
    channel.queue_bind(exchange="orders.sync", queue="api_users_orders")

    def callback(ch, method, properties, body):
        try:
            data = json.loads(body)
            action = data.get("action")
            order_id = data.get("order_id")
            order_data = data.get("data")

            db = SessionLocal()
            if action == "create":
                print(f"[x] Reçu création commande : {data}")
                create_order(db, order_id, order_data)

            elif action == "update":
                print(f"[x] Reçu mise à jour commande : {data}")
                update_order(db, order_id, order_data)

            elif action == "delete":
                print(f"[x] Reçu suppression commande : {data}")
                delete_order(db, order_id)

            else:
                print(f"[!] Action inconnue : {action}")

        except json.JSONDecodeError:
            print("[!] Impossible de parser le message JSON")
        except Exception as e:
            print(f"[!] Erreur : {e}")
        finally:
            db.close()

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue="api_users_orders", on_message_callback=callback)

    try:
        print("[*] En attente de messages... Ctrl+C pour arrêter.")
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Arrêt du consumer.")
        channel.stop_consuming()
        connection.close()

def receive_product_message():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    channel.exchange_declare(exchange="products.sync", exchange_type="fanout")
    channel.queue_declare(queue="api_users_products", durable=True)
    channel.queue_bind(exchange="products.sync", queue="api_users_products")

    def callback(ch, method, properties, body):
        try:
            data = json.loads(body)
            action = data.get("action")
            product_id = data.get("product_id")
            product_data = data.get("data")

            db = SessionLocal()

            if action == "create":
                print(f"[x] Reçu création produit : {data}")
                create_product(db, product_id, product_data)

            elif action == "update":
                print(f"[x] Reçu mise à jour produit : {data}")
                update_product(db, product_id, product_data)

            elif action == "delete":
                print(f"[x] Reçu suppression produit : {data}")
                delete_product(db, product_id)

            else:
                print(f"[!] Action inconnue : {action}")

        except json.JSONDecodeError:
            print("[!] Impossible de parser le message JSON")
        except Exception as e:
            print(f"[!] Erreur : {e}")
        finally:
            db.close()

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue="api_users_products", on_message_callback=callback)

    try:
        print("[*] En attente de messages produits... Ctrl+C pour arrêter.")
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Arrêt du consumer.")
        channel.stop_consuming()
        connection.close()