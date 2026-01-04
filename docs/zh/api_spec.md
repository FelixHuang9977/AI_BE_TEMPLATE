# API 規格書

## 1. API 目標與使用案例
DIAGBE API 作為 AI 診斷系統的後端介面，其主要目標包括：
*   **測試管理**：建立、監控及管理由前端 (VI_BE) 發起的電纜組裝測試。
*   **進程編排**：生成並管理非同步的測試進程。
*   **狀態持久化**：為舊版診斷腳本儲存及讀取 FIM (Fiber Interface Module) 狀態。
*   **結果處理**：提供測試結果存取並協助清理作業。

常見使用案例：
*   VI_BE 請求針對特定電纜進行新測試。
*   VI_BE 輪詢正在進行中的測試狀態。
*   舊版腳本在測試過程中儲存中間狀態。
*   管理員清除舊日誌與結果。

## 2. API 列表

| 端點 | 方法 | 描述 |
| :--- | :--- | :--- |
| `/api/v1/assemble_test` | POST | 建立新的組裝測試。 |
| `/api/v1/assemble_test/{test_id}` | GET | 獲取組裝測試狀態。 |
| `/api/v1/assemble_test/{test_id}` | DELETE | 取消測試。 |
| `/api/v1/assemble_test_clear_old_result` | POST | 清除舊測試結果。 |
| `/api/v1/fim_state` | GET | 獲取所有 FIM 狀態。 |
| `/api/v1/fim_state/{rack_sn}` | GET | 獲取特定機櫃的 FIM 狀態。 |
| `/api/v1/fim_state/{rack_sn}/{test_round_id}` | GET | 獲取特定輪次的 FIM 狀態。 |
| `/api/v1/fim_state/{rack_sn}/{test_round_id}` | POST | 更新 FIM 狀態。 |
| `/api/v1/fim_state/{rack_sn}/{test_round_id}` | DELETE | 刪除 FIM 狀態。 |

## 3. 個別 API 詳情

### /api/v1/assemble_test

#### **POST** /api/v1/assemble_test
建立新的組裝測試。
*   **請求本體**:
    ```json
    {
        "cable_uid": "string",
        "test_data": "string",
        "test_id": "string"  // 可選。若存在則使用之；若不存在則創建新 ID；若已存在且衝突則返回錯誤
    }
    ```
*   **回應本體**:
    ```json
    {
        "cable_uid": "string",
        "test_id": "string",
        "test_status": "string" // "pending", "in_progress", "completed", "error"
    }
    ```
*   **描述**: 建立新測試 ID，分叉測試進程，並立即返回。

### /api/v1/assemble_test/{test_id}

#### **GET** /api/v1/assemble_test/{test_id}
獲取組裝測試狀態。
*   **回應本體**:
    ```json
    {
        "cable_uid": "string",
        "test_id": "string",
        "test_status": "string"
    }
    ```
*   **描述**: 檢查結果檔以確定當前狀態。

#### **DELETE** /api/v1/assemble_test/{test_id}
取消測試。
*   **描述**: 嘗試殺死進程並將結果標記為已刪除。

### /api/v1/assemble_test_clear_old_result

#### **POST** /api/v1/assemble_test_clear_old_result
清除舊測試結果。
*   **請求本體**:
    ```json
    {
        "days": 1
    }
    ```

### /api/v1/fim_state

#### **GET** /api/v1/fim_state
獲取所有 FIM 狀態。
*   **回應本體**:
    ```json
    {
        "all_rack": [
            {
                "rack_sn": "string",
                "test_round": [ ... ]
            }
        ]
    }
    ```

#### **GET** /api/v1/fim_state/{rack_sn}
獲取特定機櫃的 FIM 狀態。
*   **回應本體**:
    ```json
    {
        "rack_sn": "string",
        "test_round": [ ... ]
    }
    ```

#### **GET** /api/v1/fim_state/{rack_sn}/{test_round_id}
獲取特定輪次的 FIM 狀態。
*   **回應本體**: `FimStateRackItem` (與上述類似但僅包含一輪)

#### **POST** /api/v1/fim_state/{rack_sn}/{test_round_id}
更新 FIM 狀態。
*   **請求本體**:
    ```json
    {
        "rack_sn": "string",
        "test_round": [
            {
                 "test_round_id": 1,
                 "fim_state": { ... }
            }
        ]
    }
    ```
*   **描述**: 建立或更新 FIM 狀態檔 `fim_state_{rack_sn}_{test_round_id}.json`。

#### **DELETE** /api/v1/fim_state/{rack_sn}/{test_round_id}
刪除 FIM 狀態。
*   **描述**: 刪除相應的 JSON 檔案。
