import requests
import json

def send_request():
    url = "https://api.learntogoogle.de/api/counter"
    headers = {"Content-Type": "application/json"}
    data = {"page_name": "api_test_page_learntogoogle.de"}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print("Error:", response.status_code, response.text)

if __name__ == "__main__":
    send_request()