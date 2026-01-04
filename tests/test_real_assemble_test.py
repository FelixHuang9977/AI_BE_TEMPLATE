from fastapi.testclient import TestClient
from app.main import app
import pytest
import time
import os

# Create TestClient instance (simple HTTP client)
client = TestClient(app)

def test_real_assemble_process():
    """
    Test the REAL assemble test process using the actual 'assemble_test.py' script.
    No mocks are used. The backend spawns the real subprocess.
    """
    print("\n[RealTest] Starting real assemble test process verification...")

    # 1. POST /api/v1/assemble_test
    print("[RealTest] Sending POST request...")
    payload = {
        "cable_uid": "REAL-CABLE-NO-MOCK",
        "test_data": "real_data_flow"
    }
    response = client.post("/api/v1/assemble_test", json=payload)
    
    assert response.status_code == 200, f"POST failed: {response.text}"
    data = response.json()
    test_id = data["test_id"]
    print(f"[RealTest] Created Test ID: {test_id}")
    
    # 2. Monitor Status via GET /api/v1/assemble_test/{test_id}
    # The real script:
    #   - Starts
    #   - Sleeps 2s
    #   - Writes "in_progress"
    #   - Sleeps 5s
    #   - Writes "completed"
    
    # We poll for up to 15 seconds to be safe
    max_retries = 15
    final_status = None
    
    for i in range(max_retries):
        time.sleep(1) # Simple HTTP client polling delay
        
        resp_get = client.get(f"/api/v1/assemble_test/{test_id}")
        
        if resp_get.status_code == 404:
            print(f"[RealTest] Poll {i+1}: 404 Not Found (Script might be starting)")
            continue
            
        assert resp_get.status_code == 200, f"GET failed: {resp_get.text}"
        status_data = resp_get.json()
        current_status = status_data["test_status"]
        print(f"[RealTest] Poll {i+1}: Status = {current_status}")
        
        if current_status == "completed":
            final_status = "completed"
            break
        elif current_status == "error":
            final_status = "error"
            break
            
    assert final_status == "completed", f"Test did not complete successfully. Last status: {final_status}"
    print("[RealTest] Test Cycle Verified Successfully!")

if __name__ == "__main__":
    # Allow running directly if needed
    test_real_assemble_process()
