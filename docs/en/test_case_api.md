# Test Cases / 測試用例

## TC-001: Create Assemble Test Success
- **Description**: Verify valid request creates a test and spawns process.
- **Steps**:
    1. Send `POST /api/v1/assemble_test` with valid JSON.
- **Expected Result**:
    - HTTP 200 OK.
    - JSON response contains `test_id` and `status: "pending"`.
    - Process is spawned (verify by log or file creation).

## TC-002: Get Test Status Success
- **Description**: Verify retrieving status of existing test.
- **Pre-condition**: Test ID exists.
- **Steps**:
    1. Send `GET /api/v1/assemble_test/{test_id}`.
- **Expected Result**:
    - HTTP 200 OK.
    - JSON response contains correct status.

## TC-003: Get Test Status Not Found
- **Description**: Verify handling of non-existent ID.
- **Steps**:
    1. Send `GET /api/v1/assemble_test/invalid_id`.
- **Expected Result**:
    - HTTP 404 Not Found.

## TC-004: Non-blocking Execution
- **Description**: Verify API returns immediately for long-running script.
- **Steps**:
    1. Configure script to sleep for 5 seconds.
    2. Send `POST /api/v1/assemble_test`.
    3. Measure response time.
- **Expected Result**:
    - Response time < 500ms.
    - Script continues running in background.

---

## TC-001: 建立組裝測試成功
- **描述**: 驗證有效請求是否建立測試並生成進程。
- **步驟**:
    1. 發送 `POST /api/v1/assemble_test`。
- **預期結果**:
    1. HTTP 200 OK。
    2. 回傳 `test_id`。

## TC-004: 非阻塞執行
- **描述**: 驗證長運行腳本時 API 是否立即回傳。
- **步驟**:
    1. 設定腳本睡眠 5 秒。
    2. 發送 `POST`.
    3. 測量回應時間。
- **預期結果**:
    1. 回應時間 < 500ms。
    2. 腳本在背景繼續執行。
