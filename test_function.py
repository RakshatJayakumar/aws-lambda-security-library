import os
import hashlib
import requests
from my_lambda_security_lib.lambda_wrapper import (
    secure_lambda,
    start_dynamic_monitoring,
    stop_dynamic_monitoring,
)


@secure_lambda
def sample_lambda(event, context):
    secret_key = os.getenv("SECRET_KEY", "default_secret")
    with open("test_file.txt", "w") as f:
        f.write("This is a test file.")
    with open("test_file.txt", "r") as f:
        content = f.read()
    password = "SuperSecretPassword123"
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    user_input = "1 + 2"
    result = eval(user_input)
    response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
    return {"statusCode": 200, "body": "Test function executed successfully."}


def test_lambda_returns_200():
    output = sample_lambda({}, {})
    assert output["statusCode"] == 200


def test_lambda_body_not_empty():
    output = sample_lambda({}, {})
    assert output["body"] != ""
