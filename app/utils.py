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

