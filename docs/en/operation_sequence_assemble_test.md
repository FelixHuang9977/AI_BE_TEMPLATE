# Operation Sequence Diagrams / 操作時序圖

## Operation 1: Assemble Test / 線纜組裝測試
**Initiator / 發起者**: Cable Assembly Assist System (VI_BE)

```mermaid
sequenceDiagram
    participant V as VI_BE (System)
    participant D as DIAG_BE (Backend)
    participant P as Process (Script)

    Note over V, D: 1. Check/Delete Old Test (Optional)
    V->>D: Check Test Status (Optional)
    D-->>V: Return Status

    Note over V, D: 2. Create New Test
    V->>D: POST /api/v1/assemble_test {cable_uid, data}
    activate D
    D->>D: Generate test_id
    D->>P: Fork Process (Non-blocking)
    activate P
    D-->>V: Return {test_id, status: pending}
    deactivate D
    
    Note right of P: Process runs in background
    P->>P: Run Assemble Test Logic
    P->>ResultFile: Write Status (in_progress/completed)
    deactivate P
```

## Operation 2: Get Status / 獲取狀態
**Initiator / 發起者**: Shop Floor System (SFC)

```mermaid
sequenceDiagram
    participant S as SFC (System)
    participant D as DIAG_BE (Backend)
    participant F as File System

    S->>D: GET /api/v1/assemble_test/{test_id}
    activate D
    D->>F: Read .tmp.result_assemble_test_{test_id}.txt
    F-->>D: Return Content
    D-->>S: Return {test_id, status}
    deactivate D
```
