# 路由設計文件 (ROUTES.md)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 / 食譜列表 | GET | `/` 或是 `/recipes` | `templates/index.html` | 顯示所有食譜，支援搜尋與標籤過濾 |
| 新增食譜頁面 | GET | `/recipes/new` | `templates/form.html` | 顯示新增食譜表單 |
| 建立食譜 | POST | `/recipes` | — | 接收新增表單資料，寫入資料庫並重導向至首頁 |
| 食譜詳情 | GET | `/recipes/<id>` | `templates/detail.html` | 顯示單筆食譜的詳細內容與個人筆記 |
| 編輯食譜頁面 | GET | `/recipes/<id>/edit` | `templates/form.html` | 顯示編輯食譜表單，並帶入原有資料 |
| 更新食譜 | POST | `/recipes/<id>/update` | — | 接收編輯表單資料，更新資料庫並重導向至詳情頁 |
| 刪除食譜 | POST | `/recipes/<id>/delete` | — | 刪除指定食譜，重導向至首頁 |
| 查看採買清單 | GET | `/recipes/<id>/ingredients` | `templates/ingredients.html` | (擴充功能) 顯示該食譜的食材清單 |

## 2. 每個路由的詳細說明

### `GET /` 與 `GET /recipes`
- **輸入**: URL 查詢參數 `q` (搜尋關鍵字) 或 `tag` (標籤名稱)。
- **處理邏輯**: 呼叫 `Recipe.get_all()` 或 `Recipe.search()`，並獲取所有標籤供側邊欄或篩選器使用。
- **輸出**: 渲染 `templates/index.html`，傳入 `recipes` 列表與 `tags` 列表。
- **錯誤處理**: 若無資料，返回空列表並於前端顯示「目前尚無食譜」。

### `GET /recipes/new`
- **輸入**: 無。
- **處理邏輯**: 取得所有可用的標籤 `Tag.get_all()` 供使用者選擇。
- **輸出**: 渲染 `templates/form.html`，傳遞 `action="create"` 狀態。
- **錯誤處理**: 無。

### `POST /recipes`
- **輸入**: 表單欄位 `title`, `source_url`, `ingredients`, `steps`, `personal_note`, `tags[]`。
- **處理邏輯**: 
  1. 呼叫 `Recipe.create(...)`。
  2. 處理所選或新增的標籤，並呼叫 `Tag.add_to_recipe(...)` 綁定。
- **輸出**: 成功後重導向 `redirect(url_for('recipe.index'))`。
- **錯誤處理**: 若 `title`, `ingredients`, `steps` 未填，傳回 400 或重新渲染表單並顯示錯誤訊息。

### `GET /recipes/<id>`
- **輸入**: URL 變數 `id`。
- **處理邏輯**: 呼叫 `Recipe.get_by_id(id)` 與 `Tag.get_by_recipe_id(id)`。
- **輸出**: 渲染 `templates/detail.html`，傳遞 `recipe` 與 `tags`。
- **錯誤處理**: 若找不到對應 ID 的食譜，返回 404 頁面或重新導向首頁並顯示錯誤訊息。

### `GET /recipes/<id>/edit`
- **輸入**: URL 變數 `id`。
- **處理邏輯**: 呼叫 `Recipe.get_by_id(id)` 獲取原資料，並取得所有標籤及當前食譜擁有的標籤。
- **輸出**: 渲染 `templates/form.html`，傳遞 `action="edit"` 及 `recipe` 變數。
- **錯誤處理**: 若找不到對應食譜，返回 404。

### `POST /recipes/<id>/update`
- **輸入**: URL 變數 `id`，表單欄位 `title`, `source_url`, `ingredients`, `steps`, `personal_note`, `tags[]`。
- **處理邏輯**: 
  1. 呼叫 `Recipe.update(...)` 更新食譜資訊。
  2. 更新標籤關聯（可能需要先清除舊關聯再建立新關聯）。
- **輸出**: 成功後重導向 `redirect(url_for('recipe.detail', id=id))`。
- **錯誤處理**: 若必填欄位缺失，重回編輯頁並顯示提示。

### `POST /recipes/<id>/delete`
- **輸入**: URL 變數 `id`。
- **處理邏輯**: 呼叫 `Recipe.delete(id)`（資料庫中已設定 `ON DELETE CASCADE`，會連帶刪除關聯的標籤紀錄）。
- **輸出**: 成功後重導向 `redirect(url_for('recipe.index'))`。
- **錯誤處理**: 若食譜不存在則忽略或顯示錯誤。

### `GET /recipes/<id>/ingredients`
- **輸入**: URL 變數 `id`。
- **處理邏輯**: 呼叫 `Recipe.get_by_id(id)` 取出 `ingredients`。
- **輸出**: 渲染 `templates/ingredients.html` (用於手機採買時查看)。
- **錯誤處理**: 若找不到食譜返回 404。

## 3. Jinja2 模板清單

| 模板路徑 | 繼承自 | 說明 |
| --- | --- | --- |
| `templates/base.html` | (無) | 全站共用版型，包含 `<head>`、Navbar、Footer 與引入 CSS/JS |
| `templates/index.html` | `base.html` | 首頁與食譜列表，展示所有食譜的卡片 |
| `templates/detail.html` | `base.html` | 食譜詳情頁，顯示所有製作步驟、食材與個人筆記 |
| `templates/form.html` | `base.html` | 新增/編輯食譜共用的表單頁面 |
| `templates/ingredients.html` | `base.html` | 專門顯示採買清單的簡化頁面 |

## 4. 路由骨架程式碼
請參考 `app/routes/` 內的 `.py` 檔案。已使用 Flask Blueprint 來組織相關路由。
