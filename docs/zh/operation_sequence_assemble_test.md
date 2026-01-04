# 操作序列: 組裝測試

## 參與者
- **VI_BE**: 線纜組裝輔助系統
- **DIAG_BE**: AI 診斷後端服務

## 序列

1. **VI_BE** 發起組裝測試請求。
   - 端點: `POST /api/v1/assemble_test`
   - 數據: `{ "cable_uid": "...", "test_data": "..." }`
2. **DIAG_BE** 接收請求。
3. **DIAG_BE** 生成唯一的 `test_id` (UUID)。
4. **DIAG_BE** 啟動後台進程。
   - 命令: `python assemble_test.py [cable_uid] [test_data] [test_id]` (或 .bat/.sh)
   - 此操作為非阻塞。
5. **DIAG_BE** 立即響應 **VI_BE**。
   - 狀態碼: `200 OK`
   - 數據: `{ "test_id": "...", "status": "pending" }`

## 後台處理
- 啟動的進程執行測試邏輯。
- 完成後，它將結果寫入 `scripts/.tmp.result_assemble_test_{test_id}.txt`。
