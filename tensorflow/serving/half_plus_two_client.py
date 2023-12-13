import random
import requests
import sys

def batch_predict(n):
    # Generate 1000 random floating-point numbers
    numbers = [random.uniform(1.0, 10000.0) for _ in range(n)]

    # Convert the list of numbers to a comma-separated string
    # Print the result
    instances = {
        "instances": numbers
    }
    api_url = "http://localhost:8501/v1/models/half_plus_two:predict"
    try:
        response = requests.post(api_url, json=instances)
    except:
        sys.exit(1)
    if response.status_code != 200:
        sys.exit(1)
    print(f'{n:,} Predictions Response Time: {response.elapsed}')

if __name__ == "__main__":
    batch_predict(1000)
    batch_predict(10000)
    batch_predict(100000)
    batch_predict(1000000)
    batch_predict(10000000)
