# Operation 2: Check Status (Initiator: VI_BE)

```mermaid
sequenceDiagram
    participant VI_BE
    participant DIAG_BE
    participant Filesystem
    
    VI_BE->>DIAG_BE: GET /api/v1/assemble_test/{test_id}
    DIAG_BE->>Filesystem: Read .tmp.result file
    Filesystem-->>DIAG_BE: Return Content
    DIAG_BE-->>VI_BE: Return Status (pending/in_progress/completed/error)
```
