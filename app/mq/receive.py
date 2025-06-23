import pika
import json
from models import CustomerDB

def receive_order_update():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    # Assure que l'exchange existe
    channel.exchange_declare(exchange="orders.sync", exchange_type="fanout")

    # Déclare une queue spécifique pour cette API
    channel.queue_declare(queue="api_customers", durable=True)

    # Lie la queue à l'exchange
    channel.queue_bind(exchange="orders.sync", queue="api_customers")

    def callback(ch, method, properties, body):
        try:
            data = json.loads(body)
            if data.get("action") == "update":
                user_data = data.get("data")
                print(f"[x] Reçu mise à jour commande: {data}")
            elif data.get("action") == "create":
                # Traite la création de commande
                print(f"[x] Reçu création commande: {data}")
            elif data.get("action") == "delete":
                # Traite la suppression de commande
                print(f"[x] Reçu suppression commande: {data}")
            else:
                print(f"[!] Action inconnue dans le message: {data}")
            

        except json.JSONDecodeError:
            print("[!] Message reçu mais impossible à parser")

        # Confirme réception du message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Consommation des messages
    channel.basic_consume(queue="api_customers", on_message_callback=callback)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Arrêt du consumer.")
        channel.stop_consuming()
        connection.close()