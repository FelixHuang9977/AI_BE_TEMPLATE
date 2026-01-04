import requests
import time
import sys

BASE_URL = "http://localhost:9000"

def verify_non_blocking():
    print("Verifying Non-blocking API...")
    
    start_time = time.time()
    
    payload = {
        "cable_uid": "NON-BLOCK-TEST",
        "test_data": "data"
    }
    
    try:
        r = requests.post(f"{BASE_URL}/api/v1/assemble_test", json=payload)
        r.raise_for_status()
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"API Response Time: {duration:.4f} seconds")
        
        if duration > 1.0:
            print("FAILED: API took too long to respond. It might be blocking.")
            sys.exit(1)
        else:
            print("PASSED: API responded immediately.")
            
        data = r.json()
        test_id = data["test_id"]
        print(f"Test ID: {test_id}")
        
        # Poll for completion to ensure checking script actually ran
        print("Polling for completion (Script should take ~7s)...")
        completed = False
        for _ in range(15):
            r = requests.get(f"{BASE_URL}/api/v1/assemble_test/{test_id}")
            if r.status_code == 200:
                status = r.json().get("test_status")
                print(f"Status: {status}")
                if status == "completed":
                    completed = True
                    break
            time.sleep(1)
            
        if completed:
            print("PASSED: Process completed in background.")
        else:
            print("FAILED: Process did not complete in time.")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify_non_blocking()
