# API 規範 (diagbe)

## 摘要
**diagbe** 服務提供 RESTful API 來管理線纜組裝測試流程。它作為線纜組裝輔助系統 (VI_BE) 與後端測試執行之間的橋樑，並向車間系統 (SFC) 提供狀態更新。

API 運行在端口 **9000** 上。

## API 列表

| 方法 | 端點 | 描述 |
| :--- | :--- | :--- |
| `POST` | `/api/v1/assemble_test` | 創建新的組裝測試 |
| `GET` | `/api/v1/assemble_test/{test_id}` | 獲取組裝測試的狀態 |
| `DELETE` | `/api/v1/assemble_test/{test_id}` | 取消/刪除組裝測試 |
| `POST` | `/api/v1/assemble_test_clear_old_result` | 清除舊的結果文件 |

## API 詳情

### 1. 創建組裝測試 (Create Assemble Test)
創建一個新的組裝測試，生成測試 ID，並在後台啟動測試流程。

- **名稱**: 創建組裝測試
- **方法**: `POST`
- **URL**: `/api/v1/assemble_test`
- **描述**: 此端點發起一個新的測試會話。它分叉一個非阻塞進程來運行 `assemble_test` 腳本，並立即返回 `pending`（等待中）狀態。

#### 請求體 (Request Body)
```json
{
    "cable_uid": "string",
    "test_data": "string"
}
```

#### 響應體 (Response Body)
```json
{
    "cable_uid": "string",
    "test_id": "string",
    "process_id": "string",
    "test_status": "string"   // "pending", "in_progress", "completed", "error"
}
```

#### 示例
**請求:**
```http
POST /api/v1/assemble_test HTTP/1.1
Content-Type: application/json

{
    "cable_uid": "CABLE-2024-001",
    "test_data": "config_v1"
}
```

**響應:**
```json
{
    "cable_uid": "CABLE-2024-001",
    "test_id": "550e8400-e29b-41d4-a716-446655440000",
    "process_id": "12345",
    "test_status": "pending"
}
```

---

### 2. 獲取組裝測試狀態 (Get Assemble Test Status)
獲取特定組裝測試的當前狀態。

- **名稱**: 獲取組裝測試狀態
- **方法**: `GET`
- **URL**: `/api/v1/assemble_test/{test_id}`
- **描述**: 通過讀取結果文件 `.tmp.result_assemble_test_{test_id}.txt` 來檢查測試狀態。

#### 請求參數
- `test_id`: 測試的唯一標識符。

#### 響應體 (Response Body)
```json
{
    "cable_uid": "string",
    "test_id": "string",
    "process_id": "string",
    "test_status": "string"   // "pending", "in_progress", "completed", "failed"
}
```

#### 示例
**請求:**
```http
GET /api/v1/assemble_test/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
```

**響應:**
```json
{
    "cable_uid": "CABLE-2024-001",
    "test_id": "550e8400-e29b-41d4-a716-446655440000",
    "process_id": "12345",
    "test_status": "completed"
}
```

---

### 3. 刪除/取消組裝測試 (Delete/Cancel Assemble Test)
取消正在運行的測試或刪除測試記錄。

- **名稱**: 刪除組裝測試
- **方法**: `DELETE`
- **URL**: `/api/v1/assemble_test/{test_id}`
- **描述**: 從 `.tmp.{test_id}.pid` 讀取進程 ID，如果進程正在運行則終止它，刪除 PID 文件，並重命名結果文件以標示刪除。

#### 請求參數
- `test_id`: 測試的唯一標識符。

#### 示例
**請求:**
```http
DELETE /api/v1/assemble_test/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
```

**響應:**
*狀態碼: 200 OK* (或具體消息)

---

### 4. 清除舊結果 (Clear Old Results)
從系統中清除舊的結果文件和 PID 文件。

- **名稱**: 清除舊結果
- **方法**: `POST`
- **URL**: `/api/v1/assemble_test_clear_old_result`
- **描述**: 刪除早於指定天數的結果文件和 PID 文件。

#### 請求體 (Request Body)
```json
{
    "days": "int"
}
```
*   `days`: (可選) 保留文件的天數。默認為 1 天。如果為 0，則刪除所有。

#### 示例
**請求:**
```http
POST /api/v1/assemble_test_clear_old_result HTTP/1.1
Content-Type: application/json

{
    "days": 7
}
```

**響應:**
*狀態碼: 200 OK*
