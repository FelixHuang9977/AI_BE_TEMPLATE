
# Operation Sequence: Admin Monitor Assemble Test

This document describes the sequence of interactions for the Admin to monitor all running assemble test processes.

## Participants
- **ADMIN**: The system administrator.
- **DIAG_BE**: The Diagnosis Backend Service.

## Sequence Diagram

```mermaid
sequenceDiagram
    participant ADMIN
    participant DIAG_BE

    Note over ADMIN: Admin wants to check status of all tests

    ADMIN->>DIAG_BE: GET /api/v1/assemble_test
    activate DIAG_BE
    
    DIAG_BE-->>ADMIN: 200 OK (JSON List of Tests)
    deactivate DIAG_BE

    Note over ADMIN: Admin reviews the list (test_id, status, process_id)
```

## detailed steps
1. **ADMIN** sends a `GET` request to `/api/v1/assemble_test`.
2. **DIAG_BE** scans the `scripts` directory for tracking files.
3. **DIAG_BE** returns a list of all assemble tests with their current status.
