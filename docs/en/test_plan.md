# Test Plan / 測試計畫

## 1. Objective / 目標
To verify the functionality, performance, and reliability of the AI Diagnosis Backend Service (DIAG_BE).
驗證 AI 診斷後端服務的功能、性能和可靠性。

## 2. Scope / 範圍
- **API Functionality**: Verify POST and GET endpoints.
- **Process Management**: Verify process spawning and non-blocking behavior.
- **Integration**: Verify interaction with dummy scripts (mimicking legacy scripts).
- **API 功能**: 驗證 POST 和 GET 端點。
- **進程管理**: 驗證進程生成和非阻塞行為。
- **整合**: 驗證與虛擬腳本的互動。

## 3. Test Strategy / 測試策略
- **Unit Testing**: Use `pytest` to test API logic with mocked dependencies.
- **Integration Testing**: Use `verify_api.py` to test against a running server with actual script execution.
- **Performance Testing**: Verify the API returns immediately even if the script takes time.
- **單元測試**: 使用 `pytest` 測試 API 邏輯。
- **整合測試**: 使用 `verify_api.py` 測試運行中的伺服器。
- **性能測試**: 驗證 API 是否在腳本執行時立即回傳。

## 4. Test Environment / 測試環境
- **OS**: Windows / Linux
- **Python**: 3.8+
- **Dependencies**: `requirements.txt`

## 5. Schedule / 時程
- **TBD**
