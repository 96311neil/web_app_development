# 系統流程圖文件

本文件根據 PRD 與系統架構設計，梳理出「食譜收藏夾」系統的各項流程。

## 1. 使用者流程圖 (User Flow)

描述使用者進入系統後的主要操作路徑與邏輯分支，涵蓋主要功能如新增、查看、編輯與刪除。

```mermaid
flowchart LR
    A([使用者進入網站]) --> B[首頁 - 食譜列表]
    B --> C{選擇操作}
    
    C -->|搜尋/篩選| D[輸入關鍵字或點擊標籤]
    D --> B
    
    C -->|查看詳情| E[食譜詳細內容頁]
    E --> F{選擇操作}
    F -->|產生食材清單| G[查看/匯出食材清單]
    F -->|個人筆記| H[新增/編輯筆記]
    F -->|分享| I[複製分享連結]
    F -->|返回| B
    
    C -->|新增食譜| J[填寫新增食譜表單]
    J --> K{儲存}
    K -->|成功| B
    K -->|失敗或錯誤| J
    
    E -->|編輯食譜| L[填寫編輯食譜表單]
    L --> M{儲存}
    M -->|成功| E
    
    E -->|刪除食譜| N{確認刪除}
    N -->|是| B
    N -->|否| E
```

## 2. 系統序列圖 (Sequence Diagram)

以「使用者新增食譜」為例，描述前端操作到後端資料庫的完整互動歷程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (Frontend)
    participant Flask as Flask 路由 (Controller)
    participant Model as Recipe 模型 (Model)
    participant DB as SQLite (Database)
    
    User->>Browser: 點擊「新增食譜」，進入表單頁
    User->>Browser: 填寫表單 (名稱、食材、步驟、標籤) 並送出
    Browser->>Flask: POST /recipes
    Flask->>Flask: 驗證表單資料
    alt 資料驗證失敗
        Flask-->>Browser: 回傳錯誤訊息並保留已填寫內容
        Browser-->>User: 顯示錯誤提示
    else 資料驗證成功
        Flask->>Model: 建立 Recipe 物件
        Model->>DB: INSERT INTO recipes ...
        DB-->>Model: 成功 (回傳 ID)
        Model-->>Flask: 成功
        Flask-->>Browser: HTTP 302 重新導向至首頁
        Browser-->>User: 顯示成功訊息及更新後的列表
    end
```

## 3. 功能清單對照表

系統主要功能與對應的路由與 HTTP 方法設計。

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
| -------- | -------- | --------- | ---- |
| 瀏覽首頁/列表 | `/` 或 `/recipes` | GET | 顯示所有食譜，支援查詢參數（搜尋關鍵字、標籤過濾） |
| 新增食譜頁面 | `/recipes/new` | GET | 顯示新增食譜的 HTML 表單 |
| 送出新增食譜 | `/recipes` | POST | 接收表單資料，寫入資料庫並重導向 |
| 查看食譜詳情 | `/recipes/<id>` | GET | 顯示單筆食譜詳細內容、步驟與個人筆記 |
| 編輯食譜頁面 | `/recipes/<id>/edit` | GET | 顯示編輯食譜的 HTML 表單（帶入原有資料） |
| 送出編輯食譜 | `/recipes/<id>` | POST (或 PUT) | 更新特定食譜的資料庫記錄並重導向 |
| 刪除食譜 | `/recipes/<id>/delete` | POST (或 DELETE) | 刪除特定食譜記錄並重導向回列表頁 |
| 查看食材清單 | `/recipes/<id>/ingredients` | GET | (擴充功能) 顯示此食譜對應的採買食材清單 |
