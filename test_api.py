import requests

# Define the API endpoint
url = "http://127.0.0.1:8000/chat"

# Define the payload (JSON request)
data = {"prompt": "Tell me a joke"}

# Make a POST request to the API
response = requests.post(url, json=data)

# Print the response
print("Response from API:", response.json())
