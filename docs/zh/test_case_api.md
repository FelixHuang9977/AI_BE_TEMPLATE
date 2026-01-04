# 測試用例: API

## TC01: 創建組裝測試 (成功)
- **描述**: 驗證可以成功創建新的組裝測試。
- **輸入**: 
    - 方法: POST
    - URL: `/api/v1/assemble_test`
    - Body: `{"cable_uid": "TEST-001", "test_data": "raw_data"}`
- **預期結果**:
    - 狀態碼: 200
    - Body: 包含 `test_id` (UUID), `test_status`: "pending"。
    - 後端: 啟動後台進程。

## TC02: 獲取測試狀態 (未找到)
- **描述**: 驗證查詢不存在的 ID 返回 404。
- **輸入**:
    - 方法: GET
    - URL: `/api/v1/assemble_test/invalid-id`
- **預期結果**:
    - 狀態碼: 404

## TC03: 獲取測試狀態 (已完成)
- **描述**: 驗證查詢已完成的測試返回正確狀態。
- **前置條件**: `scripts/.tmp.result_assemble_test_{id}.txt` 存在且包含 `{"test_status": "completed"}`。
- **輸入**:
    - 方法: GET
    - URL: `/api/v1/assemble_test/{id}`
- **預期結果**:
    - 狀態碼: 200
    - Body: `test_status` 為 "completed"。
