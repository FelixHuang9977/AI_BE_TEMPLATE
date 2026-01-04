# Test Plan / 測試計畫

## 1. Objective / 目標
- Verify functionality of DIAG_BE service.
- 驗證 DIAG_BE 服務的功能。

## 2. Scope / 範圍
- API Endpoints (POST/GET).
- Process Management (Non-blocking).
- State transitions (Pending -> In Progress -> Completed/Error).

## 3. Strategy / 策略
- **Unit/Integration**: `pytest` with mock scripts (`mock_*.py`).
- **Real Process**: `pytest` with real script (`assemble_test.py`) using `TestClient` (No Mocks).
- **Manual**: Validation scripts.

## 4. Environment / 環境
- Local Dev (Windows/Linux).
