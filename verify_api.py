import requests
import time
import sys

BASE_URL = "http://localhost:9000"

def test_api():
    print("Starting API Verification...")
    
    # Wait for server to be up
    for i in range(10):
        try:
            r = requests.get(BASE_URL + "/")
            if r.status_code == 200:
                print("Server is up!")
                break
        except:
            time.sleep(1)
            print("Waiting for server...")
    else:
        print("Server failed to start.")
        return

    # 1. Create Assemble Test
    print("\n[TEST] Creating Assemble Test...")
    payload = {
        "cable_uid": "CABLE-123",
        "test_data": "some_test_data"
    }
    
    try:
        r = requests.post(f"{BASE_URL}/api/v1/assemble_test", json=payload)
        r.raise_for_status()
        data = r.json()
        test_id = data["test_id"]
        print(f"Test Created. ID: {test_id}, Status: {data['test_status']}")
    except Exception as e:
        print(f"Failed to create test: {e}")
        return

    # 2. Poll Status
    print("\n[TEST] Polling Status...")
    for _ in range(10):
        try:
            r = requests.get(f"{BASE_URL}/api/v1/assemble_test/{test_id}")
            if r.status_code == 200:
                status_data = r.json()
                print(f"Status: {status_data['test_status']}")
                if status_data['test_status'] == 'completed':
                    print("Test Completed Successfully!")
                    break
                elif status_data['test_status'] == 'error':
                    print("Test Failed with Error!")
                    break
            else:
                print(f"Status poll failed: {r.status_code}")
        except Exception as e:
            print(f"Polling error: {e}")
            
        time.sleep(1)

if __name__ == "__main__":
    test_api()
