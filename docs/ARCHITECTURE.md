# 系統架構設計

根據 PRD 提出的需求，以下為「食譜收藏夾」系統的技術架構與資料夾結構設計。

## 1. 技術架構說明

### 選用技術與原因
- **後端：Python + Flask**  
  Flask 是一個輕量、靈活的微框架，學習曲線平緩，不會綁定過多不必要的元件，非常適合中小型專案或個人應用的快速開發。
- **模板引擎：Jinja2**  
  Jinja2 是 Flask 內建支援的模板引擎，能將後端 Python 處理好的資料無縫注入 HTML 中。因為此專案不需要前後端分離，透過寫伺服器端渲染 (SSR) 頁面能大幅簡化開發流程。
- **資料庫：SQLite**  
  輕量級關聯式資料庫，不需啟動獨立的資料庫伺服器，將資料直接儲存於本地檔案中，適合供個人使用、資料量規模不大的食譜系統，且方便備份。
- **前端呈現：HTML, Vanilla CSS, JS**  
  前端不使用複雜框架，而是透過手寫 CSS 打造高質感且響應式（Responsive）的版面，確保手機端閱覽食譜的體驗最佳化。

### Flask MVC 模式說明
雖然 Flask 本身是微框架，但我們仍會採用類似 MVC（Model-View-Controller）的形式來組織程式碼：
- **Model (模型)**：負責與 SQLite 溝通，定義資籵表結構（例如：食譜 `Recipe`、標籤 `Tag`）。
- **View (視圖)**：負責呈現給使用者的介面，在這裡是由 `templates/` 資料夾內的 Jinja2 HTML 模板扮演此角色。
- **Controller (控制器)**：負責接聽網頁請求（Routes），從 Model 提取資料後，再丟給 View 去編譯並回傳給用戶的瀏覽器。

---

## 2. 專案資料夾結構

為了讓維護更容易且職責獨立，我們會建立以下的資料夾樹狀結構：

```text
recipe_collection/
├── app/
│   ├── __init__.py      # Flask app 初始化與設定，包含資料庫綁定
│   ├── models/          # 資料庫模型 (Model)
│   │   └── recipe.py    # 食譜、標籤等資料表定義
│   ├── routes/          # 路由與視圖邏輯 (Controller)
│   │   └── recipe.py    # 新增/編輯/搜尋食譜等端點
│   ├── templates/       # HTML 模板檔案 (View)
│   │   ├── base.html    # 共用版型 (標題、選單)
│   │   ├── index.html   # 首頁/食譜列表頁
│   │   ├── detail.html  # 食譜詳細內容頁
│   │   └── form.html    # 新增/編輯食譜頁
│   └── static/          # 靜態資源檔案
│       ├── css/         # Vanilla CSS 樣式表檔案
│       ├── js/          # 前端互動 JavaScript (如食材整理功能)
│       └── images/      # 網站圖示、預設圖片
├── instance/
│   └── database.db      # SQLite 本地資料庫檔案 (由程式自動建置)
├── docs/                # 專案文件
│   ├── PRD.md           # 產品需求文件
│   └── ARCHITECTURE.md  # 系統架構文件 (本文)
├── app.py               # 應用程式進入點與啟動檔
├── requirements.txt     # Python 依賴套件表
└── README.md            # 專案開發說明檔
```

---

## 3. 元件關係圖

以下表示使用者透過瀏覽器操作食譜收藏夾時，系統各元件之間的互動邏輯。

```mermaid
flowchart TD
    Browser[使用者瀏覽器] <--> |1. HTTP Request/Response| Router[Flask Route Controller\n(routes/)]
    
    subgraph 後端系統
        Router --> |2. 查詢/寫入資料| Model[Model 模型\n(models/)]
        Model <--> |3. 讀寫操作| DB[(SQLite 庫\ninstance/database.db)]
        Router --> |4. 傳送資料變數| Template[Jinja2 Template\n(templates/)]
    end
    
    Template --> |5. 渲染並產出 HTML| Browser
```

---

## 4. 關鍵設計決策

1. **單體架構 (Monolithic) 不做前後端分離**  
   對於單人使用的工具型系統來說，前端與後端分離會增加不必要的開發與維護成本。利用 Jinja2 的模板繼承 (Template Inheritance) 系統，已足以做到快速的介面開發與程式碼共用。

2. **採用 SQLite 減輕維運成本**  
   使用 SQLite 表示資料庫就只是一個 `instance/database.db` 檔案，當使用者想在不同電腦開發或備份整個系統時，只要直接複製檔案即可，對於單人專案是首選。

3. **Vanilla CSS 設計行動優先 (Mobile First) 介面**  
   因為使用者大部分會在「廚房」使用這個系統（使用手機查看食譜），系統必須高度依賴 RWD 響應式佈局。手刻 Vanilla CSS 能精準掌握各個元素的縮放，同時能落實高質感與無負擔的介面。

4. **藍圖機制 (Flask Blueprints) 擴展性**  
   雖然目前分為簡單的 `routes/`，但會採用 Flask Blueprint 的方式來註冊路由，這樣當未來要加入「會員系統」或「API 匯出服務」時，能直接橫向增添新的路由模組而不影響現有的食譜程式碼。
