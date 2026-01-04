
import pytest
import os
import shutil
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

@pytest.fixture
def mock_fs_for_list(tmp_path):
    # Setup some test data
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    
    # Test 1: Active
    test_id_1 = "test-1"
    pid_file_1 = scripts_dir / f".tmp.{test_id_1}.pid"
    pid_file_1.write_text("1234")
    # No result file => in_progress
    
    # Test 2: Completed
    test_id_2 = "test-2"
    pid_file_2 = scripts_dir / f".tmp.{test_id_2}.pid"
    pid_file_2.write_text("5678")
    
    res_file_2 = scripts_dir / f".tmp.result_assemble_test_{test_id_2}.txt"
    res_data_2 = {"cable_uid": "CABLE-2", "test_status": "completed"}
    res_file_2.write_text(json.dumps(res_data_2))
    
    return scripts_dir

def test_get_all_assemble_tests(mock_fs_for_list):
    with patch("app.main.utils.get_scripts_dir", return_value=str(mock_fs_for_list)):
        response = client.get("/api/v1/assemble_test")
        assert response.status_code == 200
        data = response.json()
        
        assert "all_test" in data
        items = data["all_test"]
        assert len(items) == 2
        
        # Verify item 1
        item1 = next((i for i in items if i["test_id"] == "test-1"), None)
        assert item1
        assert item1["process_id"] == "1234"
        assert item1["test_status"] == "in_progress"
        
        # Verify item 2
        item2 = next((i for i in items if i["test_id"] == "test-2"), None)
        assert item2
        assert item2["process_id"] == "5678"
        assert item2["test_status"] == "completed"
        assert item2["cable_uid"] == "CABLE-2"
