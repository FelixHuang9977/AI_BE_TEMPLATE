# 設計規格書

## 1. 系統概述
DIAGBE 是 AI 診斷系統的後端服務，負責管理光纖電纜組裝測試流程。它充當電纜組裝輔助系統 (VI_BE)、車間系統 (SFC) 和舊版診斷腳本 (DIAG_SW) 之間的介面。

## 2. 參與者
*   **DIAG_BE**: 後端服務 (FastAPI)。
*   **VI_BE**: 前端服務 (電纜組裝輔助系統)。
*   **SFC**: 車間系統。
*   **DIAG_SW**: 舊版診斷腳本。
*   **ADMIN**: 系統管理員。
*   **OPERATOR**: 組裝操作員。

## 3. 操作
*   **Operation 1 (組裝測試)**: VI_BE 請求建立測試。DIAG_BE 建立測試 ID，分叉進程執行測試腳本，並立即返回。
*   **Operation 2 (檢查狀態)**: VI_BE 輪詢 DIAG_BE 獲取測試狀態 (pending, in_progress, completed, error)。
*   **Operation 3 (推送結果)**: DIAG_SW 推送結果到 SFC。
*   **Operation 4 (Admin Ops)**: ADMIN 取消/停止測試或清除舊結果。
*   **FIM 狀態管理**: 根據機櫃序號 (Rack SN) 和測試輪次 (Test Round ID) 管理 FIM 狀態 (查詢/更新/刪除)。

## 4. 數據流
*   VI_BE -> DIAG_BE: 建立測試，獲取狀態。
*   DIAG_BE -> DIAG_SW: 分叉進程 (模擬/真實)。
*   DIAG_SW -> 文件系統: 寫入狀態/結果。
*   DIAG_BE -> 文件系統: 讀取狀態/結果。
*   DIAG_BE -> 文件系統: 讀取/寫入 FIM 狀態 (JSON)。
