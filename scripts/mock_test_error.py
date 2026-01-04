import sys
import time
import os
import json

if len(sys.argv) < 4:
    sys.exit(1)

cable_uid = sys.argv[1]
test_data = sys.argv[2]
test_id = sys.argv[3]

# Write error
result = {
    "cable_uid": cable_uid,
    "test_id": test_id,
    "test_status": "error"
}
with open(f".tmp.result_assemble_test_{test_id}.txt", "w") as f:
    json.dump(result, f)
