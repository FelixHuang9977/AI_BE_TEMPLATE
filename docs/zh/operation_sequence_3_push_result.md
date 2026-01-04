# Operation 3: Push Result (Initiator: DIAG_SW)

```mermaid
sequenceDiagram
    participant DIAG_SW
    participant DIAG_BE
    participant SFC
    
    Note over DIAG_SW: 舊版腳本邏輯
    DIAG_SW->>SFC: 推送結果 (直接或透過 Wrapper)
    Note over DIAG_SW: 根據 prompt v1，DIAG_BE api 不直接參與推送邏輯，\n但 Operation 3 說 "legacy script call DIAG_BE api to push result"
    Note over DIAG_BE: 實際上，prompt 說 "legacy diagnosis scripts call DIAG_BE api to push test result"
    
    DIAG_SW->>DIAG_BE: POST /api/v1/fim_state (保存狀態)
    DIAG_BE->>Filesystem: 寫入 FIM State JSON
```
