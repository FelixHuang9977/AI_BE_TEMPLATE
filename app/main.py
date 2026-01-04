from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import os
import subprocess
import uuid
import sys
from typing import Optional
from . import utils

app = FastAPI()

# Data Models
class AssembleTestRequest(BaseModel):
    cable_uid: str
    test_data: str

class AssembleTestResponse(BaseModel):
    cable_uid: str
    test_id: str
    test_status: str

class AssembleTestStatusResponse(BaseModel):
    cable_uid: str
    test_id: str
    test_status: str

# Configuration
PORT = 9000
    
@app.get("/")
def read_root():
    return {"message": "AI Diagnosis Backend Service"}

@app.post("/api/v1/assemble_test", response_model=AssembleTestResponse)
async def create_assemble_test(request: AssembleTestRequest, background_tasks: BackgroundTasks):
    cable_uid = request.cable_uid
    test_data = request.test_data
    test_id = str(uuid.uuid4())
    
    # Locate script
    # base_dir is app/, so scripts/ is ../scripts
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    scripts_dir = os.path.join(project_root, "scripts")
    
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

@app.get("/api/v1/assemble_test/{test_id}", response_model=AssembleTestStatusResponse)
async def get_assemble_test_status(test_id: str):
    # Check for result file
    # Format: result_assemble_test_{test_id}.txt
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    scripts_dir = os.path.join(project_root, "scripts")
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
