# Operation 1: Assemble Test (Initiator: VI_BE)

```mermaid
sequenceDiagram
    participant VI_BE
    participant DIAG_BE
    participant DIAG_SW
    
    VI_BE->>DIAG_BE: POST /api/v1/assemble_test
    DIAG_BE->>DIAG_BE: 生成 test_id
    DIAG_BE->>DIAG_SW: 分叉進程 (異步)
    DIAG_BE-->>VI_BE: 返回 test_id (立即)
    DIAG_SW->>Filesystem: 寫入狀態 (in_progress)
```
