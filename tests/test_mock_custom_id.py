
import pytest
import os
import time
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

@pytest.fixture
def mock_fs_custom_id(tmp_path):
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    
    # Create assemble_test.py
    script_path = scripts_dir / "assemble_test.py"
    script_path.write_text("print('mock script')")
    
    return scripts_dir

def test_create_with_custom_id(mock_fs_custom_id):
    scripts_dir = mock_fs_custom_id
    custom_id = "my-custom-test-id-123"
    
    with patch("app.main.utils.get_scripts_dir", return_value=str(scripts_dir)):
        # 1. Create with custom ID
        response = client.post("/api/v1/assemble_test", json={
            "cable_uid": "CABLE-X",
            "test_data": "demo",
            "test_id": custom_id
        })
        assert response.status_code == 200
        data = response.json()
        assert data["test_id"] == custom_id
        assert data["test_status"] == "pending"
        
        # Verify file creation (PID file usually created by the app logic in main -> utils)
        # Note: creates background task. We need to wait or verify task execution?
        # The main.py calls background_tasks.add_task(utils.run_assemble_test_process...)
        # run_assemble_test_process spawns subprocess which writes nothing? 
        # Actually the process writes nothing unless it's the real script.
        # But our mock just writes "mock script"
        # However, create_assemble_test does NOT create the PID file directly?
        # Wait, the prompt says: "backend ... will fork a process ... record process id, save process_id to .tmp.{test_id}.pid"
        # Let's check utils.py run_assemble_test_process? 
        # utils.py uses subprocess.Popen. It does NOT save the PID file!
        # Wait, let me check utils.py again.
        
        # Verify PID file creation (wait for background task)
        pid_file = scripts_dir / f".tmp.{custom_id}.pid"
        for _ in range(10):
            if pid_file.exists():
                break
            time.sleep(0.1)
            
        assert pid_file.exists()
        assert pid_file.read_text().strip().isdigit()

def test_create_duplicate_custom_id(mock_fs_custom_id):
    scripts_dir = mock_fs_custom_id
    custom_id = "duplicate-id"
    
    # Create existing PID file to simulate existing test
    pid_file = scripts_dir / f".tmp.{custom_id}.pid"
    pid_file.write_text("9999")
    
    with patch("app.main.utils.get_scripts_dir", return_value=str(scripts_dir)):
        response = client.post("/api/v1/assemble_test", json={
            "cable_uid": "CABLE-X", 
            "test_data": "demo", 
            "test_id": custom_id
        })
        assert response.status_code == 400
        assert "Test ID already exists" in response.json()["detail"]
