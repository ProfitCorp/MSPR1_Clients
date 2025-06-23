import pika
import json

def publish_user_update(user_id: int, data: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Déclare l'exchange (type fanout = broadcast à toutes les queues)
    channel.exchange_declare(exchange='users.sync', exchange_type='fanout')

    # Message à envoyer
    message = json.dumps({
        "action": "update",
        "user_id": user_id,
        "data": data
    })

    # Publie dans l'exchange
    channel.basic_publish(
        exchange='users.sync',
        routing_key='',  # fanout ignore la routing_key
        body=message
    )

    print(f" [x] Envoyé : {message}")
    connection.close()


def publish_user_delete(user_id: int):
    """Publie un message de suppression d'utilisateur."""
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Déclare l'exchange (type fanout = broadcast à toutes les queues)
    channel.exchange_declare(exchange='users.sync', exchange_type='fanout')

    # Message à envoyer
    message = json.dumps({
        "action": "delete",
        "user_id": user_id
    })

    # Publie dans l'exchange
    channel.basic_publish(
        exchange='users.sync',
        routing_key='',  # fanout ignore la routing_key
        body=message
    )

    print(f" [x] Envoyé : {message}")
    connection.close()
