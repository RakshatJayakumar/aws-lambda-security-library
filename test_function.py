import os
import hashlib
import requests
from my_lambda_security_lib.lambda_wrapper import secure_lambda, start_dynamic_monitoring, stop_dynamic_monitoring

@secure_lambda
def test_function(event, context):
    print("Test function has started.")
    
    # 2. Environment variable access
    secret_key = os.getenv("SECRET_KEY", "default_secret")
    print(f"Secret Key: {secret_key}")

    # 3. File operation: Write to a file
    with open("test_file.txt", "w") as file:
        file.write("This is a test file.")

    # 4. File operation: Read from a file
    with open("test_file.txt", "r") as file:
        content = file.read()
    print(f"File Content: {content}")

    # 5. Hashing operation (security-sensitive)
    # Introducing a weak cryptographic algorithm (MD5)
    password = "SuperSecretPassword123"
    hashed_password = hashlib.md5(password.encode()).hexdigest()  # This should be flagged
    print(f"Hashed Password (MD5): {hashed_password}")

    # Introducing the use of eval() which is a security risk
    user_input = "1 + 2"
    result = eval(user_input)  # This should be flagged
    print(f"Eval result: {result}")

    # 6. Network operation: HTTP GET request
    response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
    print(f"HTTP GET Response: {response.status_code}, Content: {response.json()}")

    # 7. Exception Handling
    try:
        result = 10 / 0  # This will raise an exception
    except ZeroDivisionError as e:
        print(f"Caught an exception: {e}")

    # 8. Return a result
    return {
        "statusCode": 200,
        "body": "Test function executed successfully."
    }

if __name__ == "__main__":
    # Simulate a Lambda event and context
    event = {}
    context = {}
    # Call the test function
    output = test_function(event, context)
    print(f"Function Output: {output}")
