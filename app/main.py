from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import os
import subprocess
import uuid
import sys
from typing import Optional, List, Dict, Any
from . import utils

app = FastAPI()

# Data Models
class AssembleTestRequest(BaseModel):
    cable_uid: str
    test_data: str
    test_id: Optional[str] = None

class AssembleTestResponse(BaseModel):
    cable_uid: str
    test_id: str
    test_status: str



class AssembleTestItem(BaseModel):
    cable_uid: str
    test_id: str
    process_id: str
    test_status: str

class AssembleTestListResponse(BaseModel):
    all_test: List[AssembleTestItem]

class AssembleTestStatusResponse(BaseModel):
    cable_uid: str
    test_id: str
    test_status: str

# FIM State Models
class FimStateItem(BaseModel):
    test_round_id: int
    fim_state: Dict[str, Any]

class FimStateRequest(BaseModel):
    fim_state: Dict[str, Any]
    # rack_sn and test_round_id are in URL, redundant data in body per spec note but let's make it optional or just accept it if caller sends it
    # Spec says: "keep the redundant data (rack_sn, test_round_id) for get/set; the caller can parse it easily"
    # So the request body MIGHT contain them.
    # request body: { "rack_sn": "...", "test_round": [ ... ] } ??
    # Wait, the spec for POST says:
    # request body: { "rack_sn": "string", "test_round": [ { "test_round_id": int, "fim_state": dict } ] }
    # So I should define a model that matches that structure.
    
class FimStateRoundItem(BaseModel):
    test_round_id: int
    fim_state: Dict[str, Any]
    
class FimStateRackItem(BaseModel):
    rack_sn: str
    test_round: List[FimStateRoundItem]

class FimStateListResponse(BaseModel):
    all_rack: List[FimStateRackItem]

# For Single Rack Response: { "rack_sn": "...", "test_round": [...] } -> FimStateRackItem works

# For Single Round Response: { "rack_sn": "...", "test_round": [ { test_round_id, fim_state } ] }
# This is also FimStateRackItem structure but with 1 item in list.

class FimStateUpdateRequest(BaseModel):
    # The body for POST /api/v1/fim_state/{rack_sn}/{test_round_id}
    # Body: { "rack_sn": "...", "test_round": [ { "test_round_id": ..., "fim_state": ... } ] }
    # Plus note says keep redundant data.
    rack_sn: Optional[str] = None
    test_round: Optional[List[FimStateRoundItem]] = None
    # We might want to allow loose validation since we use URL params as truth?
    # Or strict? "update fim state for specific rack_sn and specific test_round_id".
    # Since we can parse it, let's accept validation.
    
    # Actually, simpler: just use Dict[str, Any] for flexibility if structure varies, but Model is better.
    # Let's use FimStateRackItem structure for Request too.

class ClearOldResultsRequest(BaseModel):
    days: Optional[int] = 1


# Configuration
PORT = 9000
    
@app.get("/")
def read_root():
    return {"message": "AI Diagnosis Backend Service"}

@app.post("/api/v1/assemble_test", response_model=AssembleTestResponse)
async def create_assemble_test(request: AssembleTestRequest, background_tasks: BackgroundTasks):
    cable_uid = request.cable_uid
    test_data = request.test_data
    
    # Locate script
    # Use utils to get directory (testable)
    scripts_dir = utils.get_scripts_dir()

    if request.test_id:
        test_id = request.test_id
        # Check if already exists
        # Logic: check for pid file or result file
        pid_file = os.path.join(scripts_dir, f".tmp.{test_id}.pid")
        result_file = os.path.join(scripts_dir, f".tmp.result_assemble_test_{test_id}.txt")
        
        if os.path.exists(pid_file) or os.path.exists(result_file):
             raise HTTPException(status_code=400, detail="Test ID already exists")
    else:
        test_id = str(uuid.uuid4())
    
    # Locate script
    
    command = utils.find_assemble_script(scripts_dir)
    
    if not command:
        raise HTTPException(status_code=500, detail="Assemble test script not found")
        
    # Run process in background task
    background_tasks.add_task(utils.run_assemble_test_process, command, cable_uid, test_data, test_id, scripts_dir)
    
    return AssembleTestResponse(
        cable_uid=cable_uid,
        test_id=test_id,
        test_status="pending"
    )



@app.get("/api/v1/assemble_test", response_model=AssembleTestListResponse)
async def get_all_assemble_tests():
    scripts_dir = utils.get_scripts_dir()
    return utils.get_all_assemble_tests(scripts_dir)

@app.get("/api/v1/assemble_test/{test_id}", response_model=AssembleTestStatusResponse)
async def get_assemble_test_status(test_id: str):
    # Check for result file
    # Format: result_assemble_test_{test_id}.txt
    scripts_dir = utils.get_scripts_dir()
    result_filename = os.path.join(scripts_dir, f".tmp.result_assemble_test_{test_id}.txt")
    
    if not os.path.exists(result_filename):
        # If file doesn't exist yet, it might be pending or invalid ID.
        # Assuming pending for now if we know it was created? 
        # But stateless API doesn't know if ID is valid.
        # For simplicity, if not found, we can return 404 or "pending" if we assume it exists.
        # The spec says "check the result ... from result_assemble_test_{test_id}.txt"
        # If the file is not there, maybe it's completely new or failed to start?
        # Let's return a "pending" status if file missing but maybe with a note, or 404.
        # However, usually "pending" is safer if the process is just slow to write the first bytes.
        
        # But wait, if I request a random ID, it gives me pending? That might be misleading.
        # But without a database, we can't verify existence.
        # Let's assume file creation is the source of truth for "active/done" and absence means "unknown/pending".
        # Let's return 404 for now to be safe, or "pending" if that's preferred.
        # Given the requirements, I will default to returning a default pending status or 404.
        # Requirement: "it check the result of the assemble test from result_assemble_test_{test_id}.txt"
        
        # Let's return 404 if file not found to be strict, as per standard REST.
        # BUT, the process might take a split second to write the file.
        # Let's stick to 404 Not Found implies "No result available yet" or "Invalid ID".
        raise HTTPException(status_code=404, detail="Test ID not found or result not yet available")

    try:
        import json
        with open(result_filename, "r") as f:
            data = json.load(f)
            
        return AssembleTestStatusResponse(
            cable_uid=data.get("cable_uid", "unknown"),
            test_id=test_id,
            test_status=data.get("test_status", "unknown")
        )
    except Exception as e:
        return AssembleTestStatusResponse(
            cable_uid="unknown",
            test_id=test_id,
            test_status="error"
        )

@app.delete("/api/v1/assemble_test/{test_id}")
async def delete_assemble_test(test_id: str):
    scripts_dir = utils.get_scripts_dir()
    utils.delete_assemble_test(scripts_dir, test_id)
    return {"message": "Test deleted"}

@app.post("/api/v1/assemble_test_clear_old_result")
async def clear_old_results(request: ClearOldResultsRequest):
    scripts_dir = utils.get_scripts_dir()
    utils.clear_old_results(scripts_dir, request.days)
    return {"message": "Cleanup completed"}

# FIM State Endpoints

@app.get("/api/v1/fim_state", response_model=FimStateListResponse)
async def get_all_fim_state():
    scripts_dir = utils.get_scripts_dir()
    return utils.get_all_fim_states(scripts_dir)

@app.get("/api/v1/fim_state/{rack_sn}", response_model=FimStateRackItem)
async def get_fim_state_by_rack(rack_sn: str):
    scripts_dir = utils.get_scripts_dir()
    data = utils.get_fim_states_by_rack(scripts_dir, rack_sn)
    # If no data found, it returns empty test_round list, which matches model.
    return data

@app.get("/api/v1/fim_state/{rack_sn}/{test_round_id}", response_model=FimStateRackItem)
async def get_fim_state_by_round(rack_sn: str, test_round_id: int):
    scripts_dir = utils.get_scripts_dir()
    data = utils.get_fim_state_single(scripts_dir, rack_sn, test_round_id)
    if not data:
        # Not found
        # Spec implies we should maybe return 404? Or just empty?
        # Let's return 404.
        raise HTTPException(status_code=404, detail="FIM state not found")
    return data

@app.post("/api/v1/fim_state/{rack_sn}/{test_round_id}")
async def update_fim_state(rack_sn: str, test_round_id: int, request: FimStateRackItem):
    # Validate? 
    # Extract fim_state from request.
    # Request body matches FimStateRackItem: { rack_sn, test_round: [{test_round_id, fim_state}] }
    
    # We need to find the matching round in the request body list? 
    # Or assume the body contains exactly what we need?
    # The API def says "request body: { ... }" with structure.
    # Note: "redundant data ... caller can parse it".
    # But usually caller SENDS the redundant data. 
    # We should look for the item with matching test_round_id in the list.
    
    target_state = None
    if request.test_round:
        for item in request.test_round:
            if item.test_round_id == test_round_id:
                target_state = item.fim_state
                break
                
    if target_state is None:
        # Fallback: if list has only 1 item and ID matches or implicit? 
        # Or maybe the body didn't have the correct ID?
        # Let's be strict or flexible? 
        # If not found, check if only one item exists.
        if request.test_round and len(request.test_round) == 1:
             # Check if ID in body is 0 or different? 
             # Let's trust URL params more. If body ID differs, we might warn or override.
             # Ideally we use the body's content for that ID.
             pass
    
    # If we still don't have it, maybe the client sent empty map?
    if target_state is None:
         # Treat as empty dict or error?
         # "fim_state will be defined by DIAG_SW, just treat it as raw json data"
         # If missing, maybe empty dict.
         target_state = {}

    scripts_dir = utils.get_scripts_dir()
    utils.save_fim_state(scripts_dir, rack_sn, test_round_id, target_state)
    return {"message": "Success"}

@app.delete("/api/v1/fim_state/{rack_sn}/{test_round_id}")
async def delete_fim_state(rack_sn: str, test_round_id: int):
    scripts_dir = utils.get_scripts_dir()
    deleted = utils.delete_fim_state(scripts_dir, rack_sn, test_round_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="FIM state not found")
    return {"message": "Deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
