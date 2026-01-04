# 操作序列: 獲取狀態

## 參與者
- **SFC**: 車間系統
- **DIAG_BE**: AI 診斷後端服務

## 序列

1. **SFC** 發起請求以檢查組裝測試的狀態。
   - 端點: `GET /api/v1/assemble_test/{test_id}`
2. **DIAG_BE** 接收請求。
3. **DIAG_BE** 查找與 `test_id` 關聯的結果文件。
   - 文件名: `.tmp.result_assemble_test_{test_id}.txt` (位於 `scripts/` 目錄中)。
4. **確定狀態**:
   - **情況 A: 文件存在**
     - **DIAG_BE** 讀取文件中的 JSON 內容。
     - **DIAG_BE** 返回 `200 OK` 以及測試狀態 (例如 `completed`, `failed`) 和元數據。
   - **情況 B: 文件未找到**
     - **DIAG_BE** 假設測試無效或結果尚未可用。
     - **DIAG_BE** 返回 `404 Not Found` (如果設置為這樣，目前為 404)。

## API 響應示例 (成功)
```json
{
    "cable_uid": "CABLE-001",
    "test_id": "1234-5678-90ab-cdef",
    "test_status": "completed"
}
```
