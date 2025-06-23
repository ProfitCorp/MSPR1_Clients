import pika
import json

def receive_order_update():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    # Assure que l'exchange existe
    channel.exchange_declare(exchange="users.sync", exchange_type="fanout")

    # Déclare une queue spécifique pour cette API
    channel.queue_declare(queue="api_customers", durable=True)

    # Lie la queue à l'exchange
    channel.queue_bind(exchange="users.sync", queue="api_customers")

    def callback(ch, method, properties, body):
        try:
            data = json.loads(body)
            print(f"[x] Reçu mise à jour utilisateur: {data}")

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