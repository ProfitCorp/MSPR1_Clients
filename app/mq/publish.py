import pika
import json

def publish_user_update(user_id: int, data: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    channel.exchange_declare(exchange='users.sync', exchange_type='fanout')

    message = json.dumps({
        "action": "update",
        "user_id": user_id,
        "data": data
    })

    channel.basic_publish(
        exchange='users.sync',
        routing_key='',  
        body=message
    )

    connection.close()

def publish_user_create(data: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    channel.exchange_declare(exchange='users.sync', exchange_type='fanout')

    message = json.dumps({
        "action": "create",
        "data": data
    })

    channel.basic_publish(
        exchange='users.sync',
        routing_key='',  
        body=message
    )

    connection.close()

def publish_user_delete(user_id: int):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    channel.exchange_declare(exchange='users.sync', exchange_type='fanout')

    message = json.dumps({
        "action": "delete",
        "user_id": user_id
    })

    channel.basic_publish(
        exchange='users.sync',
        routing_key='', 
        body=message
    )

    print(f" [x] Envoyé : {message}")
    connection.close()