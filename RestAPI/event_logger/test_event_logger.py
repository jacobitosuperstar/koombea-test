from typing import List, Dict, Any
import os
import json
import uuid
import pytest
from fastapi.testclient import TestClient
from httpx import Response
from RestAPI.main import app

# Adding some information to the database so when tests are ran, they can be
# ran at parallel
from .models import Event
from .views import db

test_event: Event = Event(
    user_id="1",
    description="Test",
    event_id=uuid.UUID("fe24f3a2-ae47-11ef-8513-2a70e04c3944"),
    status="NotProcessed",
)
db.add(test_event)

current_path: str = os.path.dirname(os.path.abspath(__file__))
test_cases_folder: str = os.path.join(current_path, "tests")


def json_test_cases(folder_path:str) -> List[Dict]:
    """Takes all the json files from the tests folder and picks up the test
    cases from them, creating a list with each one of the test cases.
    each test case will have:
        url, description, input, expected_output
    """
    json_files: List = []
    test_cases: List = []
    # getting all the json files from the test folder
    for file in os.listdir(folder_path):
        if file.endswith(".json"):
            json_files.append(os.path.join(folder_path, file))
    # looping over each json file to pick up the test cases
    for json_file in json_files:
        with open(json_file, mode='r', encoding='UTF-8') as file:
            test_cases_file: Dict[str, Any] = json.load(file)
        # appending the test cases into the test_cases list
        for test_case in test_cases_file["test_cases"]:
            print(test_case)
            test_cases.append(
                (
                    test_case["test_description"],
                    test_case["url"],
                    test_case["http_method"],
                    test_case["input"],
                    test_case["expected_output"],
                )
            )
    return test_cases

test_cases: List[Dict] = json_test_cases(test_cases_folder)


client: TestClient = TestClient(app)


def pytest_generate_tests(metafunc):
    if "input" in metafunc.fixturenames:
        metafunc.parametrize('url, http_method, test_description, input, expected_output', test_cases)


def test_server(url, http_method, test_description, input, expected_output):
    match http_method:
        case "GET":
            response: Response = client.get(url)
            assert response.status_code == expected_output["status_code"], (
                f"Expected {expected_output["status_code"]}, "
                f"but got {response.status_code} in the test case {test_description}"
            )
        case "POST":
            response: Response = client.post(
                url,
                json=input,
            )
            assert response.status_code == expected_output["status_code"], (
                f"Expected {expected_output["status_code"]}, "
                f"but got {response.status_code} in the test case {test_description}"
            )
            for key, value in response.json().items():
                assert expected_output[key] == value, (
                    f"Expected {key}: {expected_output[key]}, "
                    f"but got {key}: {value} in the test case {test_description}"
                )
        case "PUT":
            response: Response = client.put(
                url,
                json=input,
            )
            assert response.status_code == expected_output["status_code"], (
                f"Expected {expected_output["status_code"]}, "
                f"but got {response.status_code} in the test case {test_description}"
            )
            for key, value in response.json().items():
                assert expected_output[key] == value, (
                    f"Expected {key}: {expected_output[key]}, "
                    f"but got {key}: {value} in the test case {test_description}"
                )
        case _:
            print("What are you doing over here?")
