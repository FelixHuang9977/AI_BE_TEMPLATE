import sys
import time
import os
import json

# args: script_name cable_uid test_data test_id
if len(sys.argv) < 4:
    print("Usage: test_pending.py <cable_uid> <test_data> <test_id>")
    sys.exit(1)

cable_uid = sys.argv[1]
test_data = sys.argv[2]
test_id = sys.argv[3]

print(f"Pending Test: {test_id} for {cable_uid}")

# Simulate delay before even writing "in_progress" (effectively pending)
time.sleep(5)

# Write result
result = {
    "cable_uid": cable_uid,
    "test_id": test_id,
    "test_status": "in_progress"
}

with open(f".tmp.result_assemble_test_{test_id}.txt", "w") as f:
    json.dump(result, f)
