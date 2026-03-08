import requests
import time

def test():
    # Create profile
    prof = requests.post("http://127.0.0.1:8000/api/profiles", json={
        "name": "Test1",
        "os": "windows"
    }).json()

    prof_id = prof["id"]
    print("Created profile", prof_id)

    # Launch
    res = requests.post(f"http://127.0.0.1:8000/api/profiles/{prof_id}/launch")
    print("Launch response:", res.status_code, res.json())

    for i in range(5):
        res = requests.get(f"http://127.0.0.1:8000/api/profiles/{prof_id}/status")
        print(f"Status ({i}):", res.json())
        time.sleep(1)

test()
