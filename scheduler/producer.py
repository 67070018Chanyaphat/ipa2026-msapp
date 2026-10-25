import os
import pika


def produce(host, body, user, password):
    credentials = pika.PlainCredentials(user, password)
    parameters = pika.ConnectionParameters(host=host, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange="jobs", exchange_type="direct")
    channel.queue_declare(queue="router_jobs")
    channel.queue_bind(
        queue="router_jobs", exchange="jobs", routing_key="check_interfaces"
    )

    channel.basic_publish(exchange="jobs", routing_key="check_interfaces", body=body)
    connection.close()
