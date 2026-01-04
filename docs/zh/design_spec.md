# 設計規範 - DIAGBE

## 1. 簡介
本項目 (**diagbe**) 是 AI 診斷系統的後端服務。它作為管理者處理組裝測試流程，並作為舊版診斷腳本 (DIAG_SW) 與車間系統 (SFC) 通信的接口。

## 2. 技術棧
- **類型**: RESTful API 服務
- **框架**: FastAPI (Python)
- **端口**: 9000
- **進程模型**: 守護進程 (Daemon process)
- **操作系統支持**: Windows 和 Linux
- **部署方式**: Pip / Wheel
- **CI/CD**: GitHub Actions

## 3. 系統操作

### 3.1 參與者
- **DIAG_BE**: 本後端服務 (AI Diagnosis Backend)。
- **VI_BE**: 線纜組裝輔助系統 (Cable Assembly Assist System)。
- **SFC**: 車間系統 (Shop Floor System)。
- **DIAG_SW**: 舊版診斷腳本。

### 3.2 操作流程
**操作 1: 線纜組裝測試 (由 VI_BE 發起)**
1.  **檢查/刪除舊測試**: VI_BE 調用 DIAG_BE 檢查測試 ID 是否存在 (決定刪除/停止/中止)。
2.  **創建測試**: VI_BE 調用 DIAG_BE `POST /api/v1/assemble_test` 創建新測試。
3.  **進程分叉 (Fork)**: DIAG_BE 立即返回 `test_id` 並分叉一個非阻塞進程來運行實際測試 (調用 `assemble_test.py`, `.bat`, 或 `.sh`)。
4.  **監控**: DIAG_BE 監控進程狀態 (通過輪詢結果文件或其他機制)。

**操作 2: 狀態檢查 (由 SFC 發起)**
1.  **獲取狀態**: SFC 調用 DIAG_BE `GET /api/v1/assemble_test/{test_id}`。
2.  **響應**: DIAG_BE 檢查結果文件 (`.tmp.result_assemble_test_{test_id}.txt`) 並返回狀態。

## 4. API 規範

### 4.1 創建組裝測試
- **端點**: `/api/v1/assemble_test`
- **方法**: `POST`
- **請求體**:
  ```json
  {
      "cable_uid": "string",
      "test_data": "string"
  }
  ```
- **響應體**:
  ```json
  {
      "cable_uid": "string",
      "test_id": "string",
      "test_status": "string"
  }
  ```
- **描述**: 創建測試，分叉進程，並立即返回。

### 4.2 獲取組裝測試狀態
- **端點**: `/api/v1/assemble_test/{test_id}`
- **方法**: `GET`
- **響應體**:
  ```json
    {
        "cable_uid": "string",
        "test_id": "string",
        "test_status": "string"
    }
  ```
- **描述**: 檢查 `.tmp.result_assemble_test_{test_id}.txt` 獲取狀態。

## 5. 實施細節
- 後端必須以 **非阻塞** 模式調用外部腳本 (`assemble_test.py/bat/sh`)。
- 在服務目錄中搜索腳本 (優先級: py > bat > sh)。
- **驗證**: 
    - `tests/test_mock_integration_states.py` 使用模擬腳本 (`scripts/mock_*.py`) 驗證狀態轉換。
    - `tests/test_real_assemble_test.py` 使用真實腳本 (`scripts/assemble_test.py`) 驗證無模擬的完整非阻塞生命週期。
