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
                
            # rack_sn is everything between 'state' and last part
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

import time

def clear_old_results(scripts_dir: str, days: int = 1):
    """
    Delete result files and PID files older than {days} days.
    If days is 0, delete all result files and PID files.
    """
    if not os.path.exists(scripts_dir):
        return

    # Files to match: .tmp.result_assemble_test_*.txt and .tmp.*.pid
    patterns = [
        os.path.join(scripts_dir, ".tmp.result_assemble_test_*.txt"),
        os.path.join(scripts_dir, ".tmp.*.pid")
    ]
    
    files_to_check = []
    for pattern in patterns:
        files_to_check.extend(glob.glob(pattern))
        
    now = time.time()
    cutoff_time = now - (days * 86400)
    
    for fpath in files_to_check:
        try:
            if days == 0:
                os.remove(fpath)
            else:
                mtime = os.path.getmtime(fpath)
                if mtime < cutoff_time:
                    os.remove(fpath)
        except Exception as e:
            print(f"Failed to remove {fpath}: {e}")

import signal

def delete_assemble_test(scripts_dir: str, test_id: str):
    """
    Deletes an assemble test.
    1. Kill process if running.
    2. Delete pid file.
    3. Rename result file to _deleted.txt
    """
    pid_file = os.path.join(scripts_dir, f".tmp.{test_id}.pid")
    result_file = os.path.join(scripts_dir, f".tmp.result_assemble_test_{test_id}.txt")
    
    # 1. Kill process
    if os.path.exists(pid_file):
        try:
            with open(pid_file, 'r') as f:
                pid_str = f.read().strip()
                if pid_str:
                    pid = int(pid_str)
                    try:
                        os.kill(pid, signal.SIGTERM)
                    except OSError:
                        pass # Process might be already dead
            
            # 2. Delete pid file
            os.remove(pid_file)
        except Exception as e:
            print(f"Error cleaning up PID {test_id}: {e}")
            
    # 3. Rename result file
    if os.path.exists(result_file):
        deleted_file = os.path.join(scripts_dir, f".tmp.result_assemble_test_{test_id}_deleted.txt")
        # If deleted file already exists, overwrite?
        if os.path.exists(deleted_file):
            try:
                os.remove(deleted_file)
            except:
                pass
        try:
            os.rename(result_file, deleted_file)
        except Exception as e:
             print(f"Error renaming result file {test_id}: {e}")
             
    return True


def get_all_assemble_tests(scripts_dir: str):
    """
    Returns a list of all assemble tests found in the scripts directory.
    Scans for .tmp.{test_id}.pid files.
    """
    pattern = os.path.join(scripts_dir, ".tmp.*.pid")
    files = glob.glob(pattern)
    
    results = []
    
    for fpath in files:
        try:
            fname = os.path.basename(fpath)
            # Format: .tmp.{test_id}.pid
            # Split by '.' -> ['', 'tmp', test_id, 'pid']
            parts = fname.split('.')
            if len(parts) < 4:
                continue
                
            test_id = parts[2]
            
            # Use get_assemble_test_status logic to get details?
            # Or just return basic info?
            # The API spec says return cable_uid, process_id, test_status
            
            # Read PID from file?
            with open(fpath, 'r') as f:
                process_id = f.read().strip()
                
            # Check for result file for status/cable_uid
            res_fname = os.path.join(scripts_dir, f".tmp.result_assemble_test_{test_id}.txt")
            
            test_status = "unknown"
            cable_uid = "unknown"
            
            if os.path.exists(res_fname):
                try:
                    with open(res_fname, 'r') as f:
                        data = json.load(f)
                        test_status = data.get("test_status", "unknown")
                        cable_uid = data.get("cable_uid", "unknown")
                except:
                    pass
            else:
                # If no result file but pid exists, maybe "pending" or "in_progress"?
                # Design prompt says "pending" or "in_progress".
                # If PID exists, it means we launched it.
                test_status = "in_progress" # Simplified assumption
            
            results.append({
                "cable_uid": cable_uid,
                "test_id": test_id,
                "process_id": process_id,
                "test_status": test_status
            })
            
        except Exception:
            continue
            
    return {"all_test": results}


