from fastapi.testclient import TestClient
from app.main import app
import os
import shutil
import pytest
from unittest.mock import patch, MagicMock

client = TestClient(app)

# We need to mock the utils because we don't want to actually spawn processes in unit tests 
# or rely on the existence of scripts in specific dirs during unit tests?
# But integration tests might want it.
# The user asked for "test cases by pytest".
# Let's do a mix or stick to unit testing the API logic with mocking.

@pytest.fixture
def mock_utils():
    with patch("app.main.utils") as mock:
        # Mock find_assemble_script to return a dummy command
        mock.find_assemble_script.return_value = ["echo", "test"]
        yield mock

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AI Diagnosis Backend Service"}

def test_create_assemble_test(mock_utils):
    payload = {
        "cable_uid": "TEST-CABLE-001",
        "test_data": "sample_data"
    }
    response = client.post("/api/v1/assemble_test", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["cable_uid"] == "TEST-CABLE-001"
    assert "test_id" in data
    assert data["test_status"] == "pending"
    assert len(data["test_id"]) > 0

def test_create_assemble_test_no_script():
    # Test failure when script not found
    with patch("app.main.utils.find_assemble_script", return_value=None):
        payload = {
            "cable_uid": "TEST- Fail",
            "test_data": "data"
        }
        response = client.post("/api/v1/assemble_test", json=payload)
        assert response.status_code == 500

def test_get_assemble_test_status_not_found():
    # If the file doesn't exist, it should return 404
    response = client.get("/api/v1/assemble_test/non_existent_id")
    assert response.status_code == 404

def test_get_assemble_test_status_success(tmp_path):
    # We need to mock the file system read or the path logic.
    # main.py looks for files in ../scripts relative to app/
    # We can mock os.path.exists and open, OR we can mock the path resolution.
    
    test_id = "test-uuid-123"
    
    # We can use patching to redirect the file read to a temp file
    # Or mock the whole get_assemble_test_status logic? No, we want to test it.
    
    # Let's mock the path construction or the file operations.
    # It constructs: scripts_dir = os.path.join(project_root, "scripts")
    # result_filename = os.path.join(scripts_dir, f".tmp.result_assemble_test_{test_id}.txt")
    
    # Easiest way is to integration test with actual files if we can control where it looks.
    # But it looks relative to __file__.
    
    # Let's patch os.path.exists and open (builtins.open).
    
    mock_data = {
        "cable_uid": "CABLE-001",
        "test_id": test_id,
        "test_status": "completed"
    }
    
    with patch("os.path.exists", return_value=True), \
         patch("builtins.open", new_callable=MagicMock) as mock_open:
        
        # Configure mock_open to return the json data
        import json
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.read.return_value = json.dumps(mock_data)
        
        response = client.get(f"/api/v1/assemble_test/{test_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["test_id"] == test_id
        assert data["test_status"] == "completed"

