# Operation 4: Admin Ops (Initiator: ADMIN)

```mermaid
sequenceDiagram
    participant ADMIN
    participant DIAG_BE
    participant Filesystem
    
    ADMIN->>DIAG_BE: DELETE /api/v1/assemble_test/{test_id}
    DIAG_BE->>Filesystem: Delete PID file, Rename result file
    
    ADMIN->>DIAG_BE: POST /api/v1/assemble_test_clear_old_result
    DIAG_BE->>Filesystem: Delete old files
```
