# Real Tests for FIM State APIs

from fastapi.testclient import TestClient
from app.main import app
from app import utils
import pytest
import os
import shutil
from unittest.mock import patch
from dotenv import load_dotenv

# Load env
load_dotenv()
BASE_URL = os.getenv("production_url_base", "http://localhost:9000")
API_KEY = os.getenv("production_api_key", "123456")

# If we strictly follow the requirement "call the API", we should probably use `requests` effectively.
# But `TestClient` is much better for CI.
# Let's verify if `test_real_assemble_test` uses requests.

client = TestClient(app)

@pytest.fixture
def temp_scripts_dir(tmp_path):
    dir_path = tmp_path / "scripts"
    dir_path.mkdir()
    return str(dir_path)

def test_fim_state_e2e(temp_scripts_dir):
    # Patch utils.get_scripts_dir to return our temp dir
    # Note: We must patch where it is USED or where it is defined. 
    # Since main calls utils.get_scripts_dir, and we imported app.main, patching app.main.utils.get_scripts_dir works if main imported utils.
    # Actually, main imports utils. So app.main.utils is the module.
    
    with patch("app.main.utils.get_scripts_dir", return_value=temp_scripts_dir):
        
        # 1. Initial State: Empty
        response = client.get("/api/v1/fim_state")
        assert response.status_code == 200
        assert response.json() == {"all_rack": []}
        
        # 2. Create State for Rack A, Round 1
        payload_1 = {
            "rack_sn": "RackA",
            "test_round": [
                {"test_round_id": 1, "fim_state": {"step": 1, "status": "pass"}}
            ]
        }
        response = client.post("/api/v1/fim_state/RackA/1", json=payload_1)
        assert response.status_code == 200
        
        # Verify file created
        expected_file_1 = os.path.join(temp_scripts_dir, "fim_state_RackA_1.json")
        assert os.path.exists(expected_file_1)
        
        # 3. Create State for Rack A, Round 2
        payload_2 = {
            "rack_sn": "RackA",
            "test_round": [
                {"test_round_id": 2, "fim_state": {"step": 1, "status": "fail"}}
            ]
        }
        response = client.post("/api/v1/fim_state/RackA/2", json=payload_2)
        assert response.status_code == 200
        
        # 4. Get Rack A (should have 2 rounds)
        response = client.get("/api/v1/fim_state/RackA")
        assert response.status_code == 200
        data = response.json()
        assert data["rack_sn"] == "RackA"
        assert len(data["test_round"]) == 2
        assert data["test_round"][0]["test_round_id"] == 1
        assert data["test_round"][1]["test_round_id"] == 2
        assert data["test_round"][0]["fim_state"]["status"] == "pass"
        
        # 5. Get Specific Round
        response = client.get("/api/v1/fim_state/RackA/2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["test_round"]) == 1
        assert data["test_round"][0]["test_round_id"] == 2
        assert data["test_round"][0]["fim_state"]["status"] == "fail"
        
        # 6. Delete Round 1
        response = client.delete("/api/v1/fim_state/RackA/1")
        assert response.status_code == 200
        assert not os.path.exists(expected_file_1)
        
        # 7. Get Rack A (should only have Round 2)
        response = client.get("/api/v1/fim_state/RackA")
        assert response.status_code == 200
        data = response.json()
        assert len(data["test_round"]) == 1
        assert data["test_round"][0]["test_round_id"] == 2
        
        # 8. Get All (should show Rack A with 1 round)
        response = client.get("/api/v1/fim_state")
        assert response.status_code == 200
        data = response.json()
        assert len(data["all_rack"]) == 1
        assert data["all_rack"][0]["rack_sn"] == "RackA"
