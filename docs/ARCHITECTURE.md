# 系統架構設計文件 (Architecture) - 食譜收藏夾系統

這份文件根據產品需求文件 (PRD) ，規劃「食譜收藏夾系統」的技術架構與資料夾結構。以協助開發團隊清楚了解系統如何組成與運作。

## 1. 技術架構說明

本系統選擇了輕量、快速開發的技術堆疊，非常適合中小型專案與概念驗證 (MVP)。

### 選用技術與原因
- **後端：Python + Flask**
  - **原因**：Flask 輕量且極具彈性，不需要複雜的設定即可快速建立 Web 應用程式。Python 語法簡單易懂，也方便後續若需要處理食材資料整理時撰寫相關邏輯。
- **模板引擎：Jinja2**
  - **原因**：作為 Flask 預設的模板引擎，它可以直接在 HTML 中嵌入 Python 變數與邏輯 (如迴圈、條件判斷)，負責將後端處理好的試算資料渲染成最終網頁，無須建立複雜的前後端分離架構。
- **資料庫：SQLite (搭配 SQLAlchemy 或原生 sqlite3)**
  - **原因**：SQLite 是輕量的關聯式資料庫，資料直接儲存在單一檔案中，無需額外安裝或建立資料庫伺服器。對於本系統的「食譜 CRUD」、「標籤」、「使用者清單」等需求，已能提供穩定且足夠的儲存能力。

### Flask MVC 模式說明
雖然 Flask 本身不強制要求特定架構，但本專案將採用類似 **MVC (Model-View-Controller)** 的概念來組織程式碼：
- **Model (模型)**：負責定義資料結構與資料庫互動，例如 User、Recipe、Tag、ShoppingList。
- **View (視圖)**：負責呈現使用者介面，這裡指的是 `Jinja2 HTML 模板`。
- **Controller (控制器)**：負責處理商業邏輯，這裡指的是 `Flask 的 Route (路由)`。它會接收使用者的請求 (如點擊按鈕)、呼叫 Model 取得資料，最後傳遞給 View 渲染出畫面。

---

## 2. 專案資料夾結構

為了保持程式碼的整潔與可維護性，採用以下目錄結構：

```text
web_app_development/
├── app/                      # 應用程式主要邏輯
│   ├── models/               # 資料庫模型 (Model) - e.g., user.py, recipe.py
│   ├── routes/               # Flask 路由處理 (Controller) - e.g., auth.py, recipe.py
│   ├── templates/            # Jinja2 HTML 模板檔 (View) - e.g., index.html, recipe_detail.html
│   └── static/               # 靜態資源檔案
│       ├── css/              # 樣式表 (包含互動式模式的特殊字體與排版)
│       ├── js/               # 前端互動邏輯 (如一鍵生成清單的動效、計時器)
│       └── images/           # 圖片資源檔 
├── instance/                 # 放置不需進版控的執行實例檔案
│   └── database.db           # SQLite 資料庫檔案
├── docs/                     # 專案說明文件 (PRD, 架構圖等)
├── .env                      # 環境變數設定檔 (如 SECRET_KEY 等)
├── requirements.txt          # Python 依賴套件清單
└── app.py                    # Flask 應用程式進入點，負責啟動伺服器與串接設定
```

---

## 3. 元件關係圖

以下展示使用者如何透過瀏覽器與本系統互動：

```mermaid
flowchart TD
    Browser[使用者瀏覽器]

    subgraph "Flask Web Server (app/)"
        Router[Flask Route (Controller)]
        Model[Database Model (Model)]
        Template[Jinja2 Template (View)]
    end

    Database[(SQLite Database\ninstance/database.db)]

    %% 請求流向
    Browser -- "1. 發送 HTTP 請求\n(例如：查看食譜清單)" --> Router
    Router -- "2. 查詢資料" --> Model
    Model -- "3. 讀取/寫入" --> Database
    Database -- "4. 回傳資料" --> Model
    Model -- "5. 將資料交給邏輯處理" --> Router
    Router -- "6. 將資料傳入模板" --> Template
    Template -- "7. 渲染 HTML" --> Router
    Router -- "8. 回傳 HTML 畫面" --> Browser
```

---

## 4. 關鍵設計決策

1. **採用單體式架構 (Monolithic) 與伺服器端渲染 (SSR)**
   - **原因**：為了在有限的開發資源下快速實現 MVP 並降低複雜度，選擇不將前後端分離，直接透過 Flask 與 Jinja2 渲染完整的 HTML 回傳給瀏覽器。這能大幅減少 API 設計的時間與跨域 (CORS) 問題。
2. **預算統計採「使用者自填」作為 MVP 版本**
   - **原因**：串接外部真實超市優惠 API 難度與變數較大。初期優先開發基本介面，允許使用者自行輸入大致金額來統計花費，快速驗證此功能對使用者的價值後再深入串聯外部服務。
3. **區隔「一般使用者」與「系統管理者」**
   - **原因**：針對食譜屬性設計，藉由帳號角色劃分，將「公版懶人食譜」交由站方或管理員維護，而用戶也能同時保有個人私有食譜，這也牽涉後續資料庫設計的角色權限。
4. **將互動式「烹飪模式」獨立為一組視圖與 CSS**
   - **原因**：由於互動式烹飪模式強調**極大字體、分頁顯示、防誤觸**，與一般食譜預覽的排版差異甚大。設計上會抽出獨立的 Jinja2 模板（如 `cooking_mode.html`）與對應的行為腳本以增強使用者體驗（UX），也因為是單純 HTML+CSS/JS 更容易做到微小動畫。
