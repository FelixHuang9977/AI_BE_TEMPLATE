
import pytest
import os
import time
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_fs(tmp_path):
    # Create some dummy files in a temp directory
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    
    # Create files
    # 1. New result file (should not be deleted)
    (scripts_dir / ".tmp.result_assemble_test_new.txt").touch()
    
    # 2. Old result file (should be deleted)
    old_res = scripts_dir / ".tmp.result_assemble_test_old.txt"
    old_res.touch()
    
    # 3. New PID file
    (scripts_dir / ".tmp.new.pid").touch()
    
    # 4. Old PID file
    old_pid = scripts_dir / ".tmp.old.pid"
    old_pid.touch()
    
    # Set mtime to 2 days ago for old files
    old_time = time.time() - (2 * 86400) - 100
    os.utime(str(old_res), (old_time, old_time))
    os.utime(str(old_pid), (old_time, old_time))
    
    return scripts_dir

def test_clear_old_results_logic(mock_fs):
    from app import utils
    
    # Run with default days=1
    utils.clear_old_results(str(mock_fs), days=1)
    
    # Check what remains
    assert (mock_fs / ".tmp.result_assemble_test_new.txt").exists()
    assert not (mock_fs / ".tmp.result_assemble_test_old.txt").exists()
    assert (mock_fs / ".tmp.new.pid").exists()
    assert not (mock_fs / ".tmp.old.pid").exists()

def test_clear_all_results_logic(mock_fs):
    from app import utils
    
    utils.clear_old_results(str(mock_fs), days=0)
    
    assert not (mock_fs / ".tmp.result_assemble_test_new.txt").exists()
    assert not (mock_fs / ".tmp.result_assemble_test_old.txt").exists()
    assert not (mock_fs / ".tmp.new.pid").exists()
    assert not (mock_fs / ".tmp.old.pid").exists()
    
def test_api_clear_old_results(mock_fs):
    # Patch get_scripts_dir to return our mock_fs path
    with patch("app.main.utils.get_scripts_dir", return_value=str(mock_fs)):
        response = client.post("/api/v1/assemble_test_clear_old_result", json={"days": 1})
        assert response.status_code == 200
        assert response.json() == {"message": "Cleanup completed"}
        
        # Verify deletion happened
        assert (mock_fs / ".tmp.result_assemble_test_new.txt").exists()
        assert not (mock_fs / ".tmp.result_assemble_test_old.txt").exists()
