# Operation Sequence: Get Status

## Participants
- **SFC**: Shop Floor System
- **DIAG_BE**: AI Diagnosis Backend Service

## Sequence

1. **SFC** initiates a request to check the status of an assembly test.
   - Endpoint: `GET /api/v1/assemble_test/{test_id}`
2. **DIAG_BE** receives the request.
3. **DIAG_BE** looks for the result file associated with the `test_id`.
   - Filename: `.tmp.result_assemble_test_{test_id}.txt` (located in the `scripts/` directory).
4. **Determine Status**:
   - **Case A: File Exists**
     - **DIAG_BE** reads the JSON content from the file.
     - **DIAG_BE** returns `200 OK` with the test status (e.g., `completed`, `failed`) and metadata.
   - **Case B: File Not Found**
     - **DIAG_BE** assumes the test is either invalid or results are not yet available.
     - **DIAG_BE** returns `404 Not Found` (or `pending` if implemented as such, currently 404).

## API Response Example (Success)
```json
{
    "cable_uid": "CABLE-001",
    "test_id": "1234-5678-90ab-cdef",
    "test_status": "completed"
}
```
