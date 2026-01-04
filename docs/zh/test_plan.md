# 測試計劃

## 1. 概述
本計劃概述了 DIAGBE 後端服務的測試策略，以驗證功能、性能和可靠性。

## 2. 測試範圍
- **組裝測試 API**: 驗證 創建 (POST)、狀態查詢 (GET)、取消 (DELETE) 端點。
- **FIM 狀態 API**: 驗證 查詢 (GET)、更新 (POST)、刪除 (DELETE) 端點。
- **進程管理**: 驗證後台進程的啟動和非阻塞行為。
- **整合測試**: 驗證與文件系統及外部腳本的互動。

## 3. 測試策略
- **模擬測試 (單元測試)**:
    - 使用 `pytest` 和 `unittest.mock`。
    - 文件: `tests/test_mock_api.py`, `tests/test_mock_fim_state.py`。
    - 重點: API 邏輯, 數據驗證, 工具函數調用。
- **真實測試 (整合測試)**:
    - 使用 `pytest` 和臨時目錄。
    - 文件: `tests/test_real_assemble_test.py`, `tests/test_real_fim_state.py`。
    - 重點: 端對端流程, 文件讀寫, 實際腳本執行。
    - **組態**: 使用 `.env` (python-dotenv) 中的變數配置 API URL 和 Key。

## 4. 測試環境
- **OS**: Windows / Linux
- **Python**: 3.8+
- **依賴項**: `requirements.txt`

## 5. 自動化
- 運行指令: `python -m pytest tests/`。
