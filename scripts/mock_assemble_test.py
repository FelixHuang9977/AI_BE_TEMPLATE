import sys
import time
import os
import json

def main():
    if len(sys.argv) < 4:
        print("Usage: assemble_test.py <cable_uid> <test_data> <test_id>")
        sys.exit(1)

    cable_uid = sys.argv[1]
    test_data = sys.argv[2]
    test_id = sys.argv[3]

    print(f"Running assemble test for Cable: {cable_uid}, TestID: {test_id}")
    
    # Define result file name
    result_filename = f".tmp.result_assemble_test_{test_id}.txt"
    
    # Simulate processing
    # Initial status: pending (managed by API return), but script starts working
    
    try:
        # Simulate some work
        time.sleep(2) 
        
        # Write "in_progress" status (optional, if we want intermediate updates)
        # But for simplicity of this dummy, we might just write completed after sleep.
        # Let's support reading intermediate status if we re-write the file.
        
        with open(result_filename, "w") as f:
            result = {
                "cable_uid": cable_uid,
                "test_id": test_id,
                "test_status": "in_progress"
            }
            json.dump(result, f)
            
        time.sleep(5) # Simulate more work
        
        # Write final status
        with open(result_filename, "w") as f:
            result = {
                "cable_uid": cable_uid,
                "test_id": test_id,
                "test_status": "completed"
            }
            json.dump(result, f)
            
        print("Test completed successfully.")
        
    except Exception as e:
        with open(result_filename, "w") as f:
            result = {
                "cable_uid": cable_uid,
                "test_id": test_id,
                "test_status": "error",
                "error_message": str(e)
            }
            json.dump(result, f)

if __name__ == "__main__":
    main()
