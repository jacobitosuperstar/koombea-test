"""For this test set to work the hole system needs to be running.
"""
import time
import pika
import requests
from requests import Response


def server_health_check()-> bool:
    """Just checks if the server is up.
    """
    response: Response = requests.get("http://web:8000/ping")
    if response.status_code != 200:
        return False
    return True

def rabbit_mq_checker() -> bool:
    """Test if the rabbitMQ service is available.
    """
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
            host="rabbit_mq",
            port="5672",
            )
        )
        connection.close()
        return True
    except Exception:
        return False

def test_main():
    """
    """
    if not server_health_check() and not rabbit_mq_checker():
        raise ValueError("Everything must be up!!")

    # creating an event
    create_response: Response = requests.post(
        "http://web:8000/events/",
        json={
            "user_id": "1",
            "description": "Integration Test."
        }
    )
    assert create_response.status_code == 200, "There was an error in the creation of the Event"

    # Giving RabbitMQ some time
    time.sleep(2)

    # Checking the created event after a time to know if it was updated
    event_id = create_response.json()["event_id"]
    response: Response = requests.get(f"http://web:8000/events/{event_id}")
    assert response.status_code == 200, "There was an error searching for the created event"
    assert response.json()["status"] == "Processed"
