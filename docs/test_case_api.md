# Test Cases / 測試用例

## TC-001: Create Test / 建立測試
- **Step**: POST `/api/v1/assemble_test`
- **Expected**: 200 OK, `test_id`, `status: pending`.

## TC-002: Check Status / 檢查狀態
- **Step**: GET `/api/v1/assemble_test/{id}`
- **Expected**: 200 OK, correct status.

## TC-003: Non-blocking / 非阻塞
- **Step**: Create test with long-running script.
- **Expected**: Immediate response.

## TC-004: State Verification / 狀態驗證
- **Step**: Mock script sets `in_progress`, then `completed`.
- **Expected**: API reflects changes.

## TC-005: Real Process Lifecycle / 真實流程生命週期
- **Step**: Run `tests/test_real_assemble_test.py` (No mocks).
- **Process**: API -> Script (Sleep 2s) -> In Progress -> Script (Sleep 5s) -> Completed.
- **Expected**: Full state transition verified via API polling.
