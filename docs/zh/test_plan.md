# 測試計劃

## 1. 概述
本計劃概述了 DIAGBE 後端服務的測試策略。

## 2. 測試範圍
- **API 測試**: 驗證 `/api/v1/assemble_test` (POST) 和 `/api/v1/assemble_test/{test_id}` (GET)。
- **集成測試**: 驗證後台進程的啟動和文件結果的生成。
- **單元測試**: 使用 `pytest` 測試內部邏輯。

## 3. 測試環境
- **OS**: Windows (開發環境), Linux (CI/目標環境)。
- **Python**: 3.8+
- **依賴項**: `fastapi`, `uvicorn`, `requests`, `httpx`。

## 4. 測試用例
詳見 `test_case_api.md`。

## 5. 自動化
- 使用 `pytest` 運行自動化測試。
- GitHub Actions CI 在每次推送時運行測試。
