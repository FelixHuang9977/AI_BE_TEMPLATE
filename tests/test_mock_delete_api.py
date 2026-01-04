
import pytest
import os
from unittest.mock import patch, MagicMock 
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_fs_for_delete(tmp_path):
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    
    test_id = "test-delete-1"
    pid_file = scripts_dir / f".tmp.{test_id}.pid"
    pid_file.write_text("123456") # Fake PID
    
    res_file = scripts_dir / f".tmp.result_assemble_test_{test_id}.txt"
    res_file.write_text("{}")
    
    return scripts_dir, test_id

def test_delete_assemble_test(mock_fs_for_delete):
    scripts_dir, test_id = mock_fs_for_delete
    
    # We need to mock os.kill because we can't kill random PIDs
    with patch("os.kill") as mock_kill, \
         patch("app.main.utils.get_scripts_dir", return_value=str(scripts_dir)):
        
        response = client.delete(f"/api/v1/assemble_test/{test_id}")
        assert response.status_code == 200
        assert response.json() == {"message": "Test deleted"}
        
        # Verify files
        assert not (scripts_dir / f".tmp.{test_id}.pid").exists()
        assert not (scripts_dir / f".tmp.result_assemble_test_{test_id}.txt").exists()
        assert (scripts_dir / f".tmp.result_assemble_test_{test_id}_deleted.txt").exists()
        
        # Verify kill was called
        # PID from file is 123456
        mock_kill.assert_called()
