from fastapi.testclient import TestClient
from app.main import app
import pytest
import os
import time
import sys
from unittest.mock import patch

client = TestClient(app)

# Helper to get script path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
scripts_dir = os.path.join(project_root, "scripts")

def get_script_command(script_name):
    script_path = os.path.join(scripts_dir, script_name)
    return [sys.executable, script_path]

@pytest.fixture
def clean_result_files():
    # Cleanup before/after
    yield
    # Cleanup logic if needed, although mostly specific to test_ids generated inside tests
    # Since we can't easily know random IDs here, we rely on temp files or ignoring them.

def test_state_pending_to_inprogress(clean_result_files):
    # Mock find_assemble_script to return mock_test_pending.py
    cmd = get_script_command("mock_test_pending.py")
    
    with patch("app.utils.find_assemble_script", return_value=cmd):
        response = client.post("/api/v1/assemble_test", json={"cable_uid": "PENDING_TEST", "test_data": "data"})
        assert response.status_code == 200
        test_id = response.json()["test_id"]
        
        # Initially pending (file might not exist or script sleeping)
        # The script sleeps 5s before writing "in_progress".
        
        # Check immediately - should be 404 (if file missing) or pending
        time.sleep(1) 
        # API returns 404 if file missing. 
        # "raise HTTPException(status_code=404, detail="Test ID not found or result not yet available")"
        r = client.get(f"/api/v1/assemble_test/{test_id}")
        assert r.status_code == 404
        
        # Wait for script to write (sleeps 5s total)
        time.sleep(6)
        r = client.get(f"/api/v1/assemble_test/{test_id}")
        assert r.status_code == 200
        assert r.json()["test_status"] == "in_progress"

def test_state_inprogress_to_completed(clean_result_files):
    # Mock find_assemble_script to return mock_test_inprogress.py
    cmd = get_script_command("mock_test_inprogress.py")
    
    with patch("app.utils.find_assemble_script", return_value=cmd):
        response = client.post("/api/v1/assemble_test", json={"cable_uid": "INPROG_TEST", "test_data": "data"})
        assert response.status_code == 200
        test_id = response.json()["test_id"]
        
        # Checks immediately -> in_progress (script writes it immediately)
        time.sleep(2) # Give a moment for process create/write
        r = client.get(f"/api/v1/assemble_test/{test_id}")
        assert r.status_code == 200
        assert r.json()["test_status"] == "in_progress"
        
        # Script sleeps 5s then writes completed
        time.sleep(6)
        r = client.get(f"/api/v1/assemble_test/{test_id}")
        assert r.status_code == 200
        assert r.json()["test_status"] == "completed"

def test_state_error(clean_result_files):
    # Mock find_assemble_script to return mock_test_error.py
    cmd = get_script_command("mock_test_error.py")
    
    with patch("app.utils.find_assemble_script", return_value=cmd):
        response = client.post("/api/v1/assemble_test", json={"cable_uid": "ERROR_TEST", "test_data": "data"})
        assert response.status_code == 200
        test_id = response.json()["test_id"]
        
        time.sleep(2)
        r = client.get(f"/api/v1/assemble_test/{test_id}")
        assert r.status_code == 200
        assert r.json()["test_status"] == "error"
