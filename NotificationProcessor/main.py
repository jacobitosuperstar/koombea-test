import os
import sys
import json
import time
import pika

def consumer(
    host: str,
    port: str,
    queue_name: str,
    routing_key: str,
    exchange: str,
):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                port=port,
            )
        )
        channel = connection.channel()
        channel.exchange_declare(
            exchange=exchange,
        )

        channel.queue_declare(
            queue=queue_name,
        )

        channel.queue_bind(
            queue=queue_name,
            exchange=exchange,
            routing_key=routing_key,
        )

        def callback(ch, method, properties, body):
            payload = json.loads(body)
            print(" [x] Received ")
            print(payload)

        channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=True
        )

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

if __name__ == "__main__":
    time.sleep(10)
    consumer(
        host="rabbit_mq",
        port="5672",
        queue_name="test",
        routing_key="test",
        exchange="test",
    )
