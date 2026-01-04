# AI Diagnosis Backend Service (DIAGBE)

這是一個用於 AI 診斷系統的後端服務，提供 RESTful API 來管理線纜組裝測試流程。

## 專案功能
- **建立測試**: 接收請求並啟動後台測試進程 (非阻塞)。
- **查詢狀態**: 查詢測試進程的執行狀態。

## 安裝

### 源碼安裝
1. 克隆存儲庫: `git clone <repository_url>`
2. 安裝依賴: `pip install -r requirements.txt`

### Wheel 安裝
1. 建立 Wheel 包: `pip install build && python -m build`
2. 安裝 Wheel 包: `pip install dist/ai_diagbe-0.1.0-py3-none-any.whl`

## 部署

### 檢查端口佔用
啟動前請確保端口 9000 未被佔用。
- **Windows**: `netstat -ano | findstr :9000`
- **Linux**: `ss -lptn | grep :9000`

### 運行服務

#### 手動啟動
```bash
python -m app.main
# 或者
uvicorn app.main:app --host 0.0.0.0 --port 9000
```

#### Systemd 服務 (Linux)
1. 複製服務文件: `sudo cp ai_diagbe.service /etc/systemd/system/`
2. 重載守護進程: `sudo systemctl daemon-reload`
3. 啟用服務: `sudo systemctl enable ai_diagbe`
4. 啟動服務: `sudo systemctl start ai_diagbe`
5. 停止服務: `sudo systemctl stop ai_diagbe`
6. 檢查狀態: `sudo systemctl status ai_diagbe`

## 開發

### Git 工作流
切換到特定分支:
```bash
git checkout <branch_name>
```

### 運行測試
使用詳細輸出運行 pytest:
```bash
pytest -v
```

#### 真實流程驗證
運行真實組裝測試流程驗證 (無模擬):
```bash
pytest -v tests/test_real_assemble_test.py
```
