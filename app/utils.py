import os
import subprocess
import sys
import platform

def find_assemble_script(base_dir: str):
    """
    Search for assemble_test.py, assemble_test.bat, or assemble_test.sh in the directory.
    Returns the full path and execution command.
    """
    # Ensure directory exists
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # Priority: py, bat, sh
    
    # 1. Python script
    py_script = os.path.join(base_dir, "assemble_test.py")
    if os.path.exists(py_script):
        return [sys.executable, py_script]
        
    # 2. Batch script
    if platform.system() == "Windows":
        bat_script = os.path.join(base_dir, "assemble_test.bat")
        if os.path.exists(bat_script):
            return [bat_script]
            
    # 3. Shell script
    sh_script = os.path.join(base_dir, "assemble_test.sh")
    if os.path.exists(sh_script):
        # On windows, we might need bash if it is available, or it might just fail if not in environment
        # But assuming standard unix-like environment or WSL/Git Bash if .sh is present
        return ["bash", sh_script] 
        
    return None

def run_assemble_test_process(command: list, cable_uid: str, test_data: str, test_id: str, base_dir: str):
    """
    Runs the assemble test process.
    Arguments are passed as command line arguments: cable_uid, test_data, test_id
    """
    try:
        # We need to pass arguments. The dummy script needs to know where to write.
        # We'll pass them as positional arguments.
        # Script signature expected: script_name cable_uid test_data test_id
        
        full_command = command + [cable_uid, test_data, test_id]
        
        # Spawn the process. 
        if platform.system() == "Windows":
             # Use cmd 'start' to detach completely
             # We need to construct a string command for shell=True
             # Quote arguments
             cmd_str = f'start /b "" "{command[0]}"'
             if len(command) > 1:
                 # Add script path
                 cmd_str += f' "{command[1]}"'
             
             # Add args
             cmd_str += f' "{cable_uid}" "{test_data}" "{test_id}"'
             
             subprocess.Popen(cmd_str, cwd=base_dir, shell=True)
             
        else:
             # On Linux/Unix
             kwargs = {}
             kwargs['start_new_session'] = True
             kwargs['close_fds'] = True
             
             subprocess.Popen(
                full_command, 
                cwd=base_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                **kwargs
             )
        
    except Exception as e:
        print(f"Failed to spawn process: {e}")

def get_scripts_dir(base_dir: str = None) -> str:
    """
    Resolves the scripts directory.
    If base_dir is provided (e.g. during tests), uses it.
    Otherwise, resolves relative to this file.
    """
    if base_dir:
        return base_dir
    
    # helper is in app/utils.py -> project_root is parent of app
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, "scripts")

# FIM State Helpers

import json
import glob

def get_all_fim_states(scripts_dir: str):
    """
    Returns a structure:
    {
        "all_rack": [
            {
                "rack_sn": "...",
                "test_round": [
                    {"test_round_id": 1, "fim_state": {...}}, ...
                ]
            }, ...
        ]
    }
    """
    pattern = os.path.join(scripts_dir, "fim_state_*_*.json")
    files = glob.glob(pattern)
    
    racks = {} # Map rack_sn to list of test_rounds
    
    for fpath in files:
        try:
            fname = os.path.basename(fpath)
            # Expected format: fim_state_{rack_sn}_{test_round_id}.json
            # Be careful with underscores in rack_sn.
            # Assuming format prefix is fixed "fim_state_" and suffix is ".json"
            # But rack_sn might have underscores. 
            # Strategy: Split by underscore, first 2 are "fim", "state". Last is "id.json". Middle is rack_sn.
            # However, simpler if we just read the file content if possible, or assume simple rack_sn.
            # Let's rely on parsing filename for structure but maybe content for validation?
            # actually, the requirement says "save to fim_state_{rack_sn}_{test_round_id}.json"
            # Let's use robust parsing if rack_sn contains underscores.
            # It ends with _{test_round_id}.json
            
            # Remove extension
            name_no_ext = os.path.splitext(fname)[0] # fim_state_{rack_sn}_{test_round_id}
            
            # Split
            parts = name_no_ext.split('_')
            if len(parts) < 4:
                continue # Invalid format
                
            test_round_id_str = parts[-1]
            try:
                test_round_id = int(test_round_id_str)
            except ValueError:
                continue
                
            # rack_sn is everthing between 'state' and last part
            # parts[0]=fim, parts[1]=state
            rack_sn = "_".join(parts[2:-1])
            
            with open(fpath, 'r') as f:
                data = json.load(f)
                fim_state = data.get("fim_state", {})
                
            if rack_sn not in racks:
                racks[rack_sn] = []
                
            racks[rack_sn].append({
                "test_round_id": test_round_id,
                "fim_state": fim_state
            })
            
        except Exception:
            continue
            
    # Format output
    all_rack_list = []
    for rack_sn, rounds in racks.items():
        # Sort rounds by id
        rounds.sort(key=lambda x: x["test_round_id"])
        all_rack_list.append({
            "rack_sn": rack_sn,
            "test_round": rounds
        })
        
    return {"all_rack": all_rack_list}

def get_fim_states_by_rack(scripts_dir: str, rack_sn: str):
    """
    Returns info for specific rack.
    """
    all_data = get_all_fim_states(scripts_dir)
    for rack in all_data["all_rack"]:
        if rack["rack_sn"] == rack_sn:
            return rack
    
    # If not found, return empty structure for that rack? or 404?
    # Spec says "get fim state for specific rack_sn". If none, maybe empty list of rounds.
    return {
        "rack_sn": rack_sn,
        "test_round": []
    }

def get_fim_state_single(scripts_dir: str, rack_sn: str, test_round_id: int):
    """
    Returns single test round info.
    """
    fname = f"fim_state_{rack_sn}_{test_round_id}.json"
    fpath = os.path.join(scripts_dir, fname)
    
    if os.path.exists(fpath):
        try:
            with open(fpath, 'r') as f:
                data = json.load(f)
                return {
                    "rack_sn": rack_sn,
                    "test_round": [
                        {
                            "test_round_id": test_round_id,
                            "fim_state": data.get("fim_state", {})
                        }
                    ]
                }
        except Exception:
            pass
            
    return None # Not found

def save_fim_state(scripts_dir: str, rack_sn: str, test_round_id: int, fim_state: dict):
    if not os.path.exists(scripts_dir):
        os.makedirs(scripts_dir)
        
    fname = f"fim_state_{rack_sn}_{test_round_id}.json"
    fpath = os.path.join(scripts_dir, fname)
    
    # Content structure as per spec? 
    # "save the fim state ... fim_state will be defined by DIAG_SW, just treat it as raw json data"
    # To be consistent with read, we wrap it? 
    # The read helpers above assumed `data.get("fim_state", {})`. 
    # So we should save `{"fim_state": ...}`
    
    data_to_save = {
        "rack_sn": rack_sn,
        "test_round_id": test_round_id,
        "fim_state": fim_state
    }
    
    with open(fpath, 'w') as f:
        json.dump(data_to_save, f, indent=4)

def delete_fim_state(scripts_dir: str, rack_sn: str, test_round_id: int):
    fname = f"fim_state_{rack_sn}_{test_round_id}.json"
    fpath = os.path.join(scripts_dir, fname)
    if os.path.exists(fpath):
        os.remove(fpath)
        return True
    return False


