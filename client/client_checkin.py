import requests
from datetime import datetime, timezone
import time

SERVER_URL = "http://127.0.0.1:8000/api/v1/check_in"

TOKEN = "YOUR_SECRET_TOKEN"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def check_in():
    payload = {
        "status": "online",
        "time": datetime.now(timezone.utc).isoformat()
    }

    try:
        response = requests.post(
            SERVER_URL,
            json=payload,
            headers=headers,
            timeout=10
        )

        print(f"Sent: {payload}")
        print(f"Server response: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")


if __name__ == "__main__":
    while True:
        check_in()
        time.sleep(30)
