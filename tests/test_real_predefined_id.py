
import pytest
import requests
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BASE_URL = os.getenv("production_url_base", "http://localhost:9000")
TEST_ID = "1"
CABLE_UID = "CABLE-REAL-TEST-1"

def test_1_cleanup_and_create():
    """
    Step 1: Cleanup any existing test with ID=1 and Create a new one.
    """
    # Cleanup
    try:
        requests.delete(f"{BASE_URL}/api/v1/assemble_test/{TEST_ID}")
    except:
        pass

    # Create
    payload = {
        "cable_uid": CABLE_UID,
        "test_data": "real_test_data",
        "test_id": TEST_ID
    }
    response = requests.post(f"{BASE_URL}/api/v1/assemble_test", json=payload)
    if response.status_code == 400 and "already exists" in response.text:
         pytest.fail(f"Test ID {TEST_ID} already exists even after cleanup attempt.")
         
    assert response.status_code == 200, f"Failed to create test: {response.text}"
    data = response.json()
    assert data["test_id"] == TEST_ID
    assert data["cable_uid"] == CABLE_UID
    assert data["cable_uid"] == CABLE_UID
    assert data["test_status"] == "pending"
    
    # Wait for the background process to start (create PID file)
    # This prevents race condition where test_2 runs before PID file exists
    for _ in range(20):
        time.sleep(0.1)
        r = requests.get(f"{BASE_URL}/api/v1/assemble_test/{TEST_ID}")
        if r.status_code == 200:
            break
    else:
        pytest.fail("Timeout waiting for test to initialize (PID file creation)")

def test_2_get_status():
    """
    Step 2: Get status of the created test.
    """
    response = requests.get(f"{BASE_URL}/api/v1/assemble_test/{TEST_ID}")
    assert response.status_code == 200
    data = response.json()
    assert data["test_id"] == TEST_ID
    assert data["test_status"] in ["pending", "in_progress", "completed"]

def test_3_stop_delete():
    """
    Step 3: Stop/Delete the test.
    """
    response = requests.delete(f"{BASE_URL}/api/v1/assemble_test/{TEST_ID}")
    assert response.status_code == 200
    
    # Verify deletion
    response = requests.get(f"{BASE_URL}/api/v1/assemble_test/{TEST_ID}")
    assert response.status_code == 404

def test_4_clear_old_results():
    """
    Step 4: Test clear old results API.
    """
    payload = {"days": 0} 
    response = requests.post(f"{BASE_URL}/api/v1/assemble_test_clear_old_result", json=payload)
    assert response.status_code == 200
