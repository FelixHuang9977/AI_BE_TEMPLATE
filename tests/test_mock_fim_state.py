# Mock Tests for FIM State APIs

from fastapi.testclient import TestClient
from app.main import app
import pytest
from unittest.mock import patch, MagicMock

client = TestClient(app)

@pytest.fixture
def mock_utils():
    with patch("app.main.utils") as mock:
        yield mock

def test_get_all_fim_state(mock_utils):
    mock_utils.get_scripts_dir.return_value = "/tmp/scripts"
    mock_utils.get_all_fim_states.return_value = {
        "all_rack": [
            {
                "rack_sn": "RACK01",
                "test_round": []
            }
        ]
    }
    
    response = client.get("/api/v1/fim_state")
    assert response.status_code == 200
    data = response.json()
    assert len(data["all_rack"]) == 1
    assert data["all_rack"][0]["rack_sn"] == "RACK01"

def test_get_fim_state_by_rack(mock_utils):
    mock_utils.get_scripts_dir.return_value = "/tmp/scripts"
    mock_utils.get_fim_states_by_rack.return_value = {
        "rack_sn": "RACK01",
        "test_round": []
    }
    
    response = client.get("/api/v1/fim_state/RACK01")
    assert response.status_code == 200
    data = response.json()
    assert data["rack_sn"] == "RACK01"

def test_get_fim_state_by_round_found(mock_utils):
    mock_utils.get_scripts_dir.return_value = "/tmp/scripts"
    mock_utils.get_fim_state_single.return_value = {
        "rack_sn": "RACK01",
        "test_round": [
            {"test_round_id": 1, "fim_state": {"foo": "bar"}}
        ]
    }
    
    response = client.get("/api/v1/fim_state/RACK01/1")
    assert response.status_code == 200
    data = response.json()
    assert data["rack_sn"] == "RACK01"
    assert data["test_round"][0]["fim_state"]["foo"] == "bar"

def test_get_fim_state_by_round_not_found(mock_utils):
    mock_utils.get_scripts_dir.return_value = "/tmp/scripts"
    mock_utils.get_fim_state_single.return_value = None
    
    response = client.get("/api/v1/fim_state/RACK01/99")
    assert response.status_code == 404

def test_update_fim_state(mock_utils):
    mock_utils.get_scripts_dir.return_value = "/tmp/scripts"
    
    payload = {
        "rack_sn": "RACK01",
        "test_round": [
            {
                "test_round_id": 1,
                "fim_state": {"status": "ok"}
            }
        ]
    }
    
    response = client.post("/api/v1/fim_state/RACK01/1", json=payload)
    assert response.status_code == 200
    
    # Verify save called
    mock_utils.save_fim_state.assert_called_once()
    args = mock_utils.save_fim_state.call_args
    # args: (scripts_dir, rack_sn, test_round_id, fim_state)
    assert args[0][1] == "RACK01"
    assert args[0][2] == 1
    assert args[0][3] == {"status": "ok"}

def test_delete_fim_state(mock_utils):
    mock_utils.get_scripts_dir.return_value = "/tmp/scripts"
    mock_utils.delete_fim_state.return_value = True
    
    response = client.delete("/api/v1/fim_state/RACK01/1")
    assert response.status_code == 200
    
def test_delete_fim_state_not_found(mock_utils):
    mock_utils.get_scripts_dir.return_value = "/tmp/scripts"
    mock_utils.delete_fim_state.return_value = False
    
    response = client.delete("/api/v1/fim_state/RACK01/1")
    assert response.status_code == 404
