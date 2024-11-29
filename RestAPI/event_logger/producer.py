"""Producer of messages that the other workers will process.
"""
from typing_extensions import TypedDict
import pika
import orjson as json

from ..settings import settings


def rabbit_mq_checker() -> bool:
    """Test if the rabbitMQ service is available.
    """
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.rabbit_mq_host,
                port=settings.rabbit_mq_port,
            )
        )
        connection.close()
        return True
    except Exception:
        return False

def rabbit_mq_sender(
    message_data: TypedDict,
    host: str,
    port: str,
    queue_name: str,
    routing_key: str,
    exchange: str,
) -> None:
    """Function for direct connection with the RabbitMQ tail.
    """
    message = json.dumps(message_data)

    try:
        # creating the sending signal of the object/message to RabbitMQ
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                port=port,
            )
        )
        channel = connection.channel()
        channel.queue_declare(
            queue=queue_name
        )
        channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=message,
        )
        connection.close()
    except Exception as e:
        print(f"Error connecting to RabbitMQ: {e}")
