# 路由與頁面設計文件 (Routes) - 食譜收藏夾系統

本文件詳細規劃了前端介面與後端 API 之間需要溝通的各項路由 (Routes)，以及其對應的 HTTP 方法與 Jinja2 HTML 模板。這將作為後續開發功能與前端版面的依據。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| **首頁** | GET | `/` | `main/index.html` | 登入後顯示個人食譜收藏；未登入重導至登入或歡迎頁 |
| **註冊頁面** | GET | `/auth/register` | `auth/register.html` | 顯示註冊表單 |
| **註冊帳號** | POST | `/auth/register` | — | 接收資料、雜湊密碼存入 DB，註冊完重導至登入 |
| **登入頁面** | GET | `/auth/login` | `auth/login.html` | 顯示登入表單 |
| **驗證登入** | POST | `/auth/login` | — | 驗證帳號密碼，設定 session，成功後重導至 `/` |
| **登出** | GET | `/auth/logout` | — | 清除 session 並重導回 `/auth/login` |
| **公版食譜探索** | GET | `/recipes/explore` | `recipe/explore.html` | 列出系統預設或公開的懶人專用食譜 |
| **新增食譜頁面** | GET | `/recipes/new` | `recipe/new.html` | 顯示食譜新增表單 (含名稱、步驟、標籤) |
| **建立食譜** | POST | `/recipes/new` | — | 接收並建立 Recipe 與 RecipeIngredient，重導至詳細頁 |
| **食譜詳細頁** | GET | `/recipes/<id>` | `recipe/detail.html` | 顯示單一獨立食譜的所有資訊 |
| **編輯食譜頁面** | GET | `/recipes/<id>/edit` | `recipe/edit.html` | 顯示編輯表單，預先填入舊資料 |
| **更新食譜** | POST | `/recipes/<id>/edit` | — | 更新至 DB，並重導向回詳細頁面 |
| **刪除食譜** | POST | `/recipes/<id>/delete` | — | 刪除指定食譜，重導至 `/` 首頁 |
| **互動式烹飪模式**| GET | `/recipes/<id>/cooking-mode`| `recipe/cooking_mode.html` | 專屬的大字體與無干擾介面，顯示步驟 |
| **購物清單總覽** | GET | `/shopping-list/` | `shopping/index.html` | 列出該使用者目前所有的購物清單與花費統計 |
| **一鍵生成清單** | POST | `/shopping-list/generate/<recipe_id>`| — | 從指定食譜拉取食材，建立或附加進現有的購物清單，重導向至清單詳情 |
| **清單詳情與編輯**| GET | `/shopping-list/<id>` | `shopping/detail.html` | 查看清單內詳情、物品是否已勾選購買與預算 |
| **更新清單項目** | POST | `/shopping-list/<list_id>/item/<item_id>`| — | 用於勾選完成、修改估算價格，然後重導向或透過 JS 發送背景請求 |

---

## 2. 路由詳細說明

### Auth (驗證模組)
- **輸入**: Form data (`username`, `email`, `password`)
- **邏輯**: 註冊時建立 `User` model；登入時使用 `check_password_hash` 驗證，並使用 Flask `session`。
- **錯誤處理**: 如果帳號已存在或密碼錯誤，透過 Flask `flash()` 顯示並 render 原模板。

### Recipe (食譜模組)
- **輸入**: Path parameters (`id`), Form data (`title`, `instructions`, ingredients array, tags array)
- **邏輯**: 新刪修查前，除了探索模式外都要加上 `@login_required`。刪除時須檢查該 Recipe 的 `user_id` 是否與當前 user 相符。
- **錯誤處理**: 找不到食譜或未授權時，回傳 404 或 403 畫面。表單未填完利用 `flash()` 提示。

### Shopping List (購物清單模組)
- **輸入**: Path parameters (`list_id`, `item_id`, `recipe_id`), 表單勾選狀態與價格預估。
- **邏輯**: 確保只撈取屬於自己的清單 (`list.user_id == current_user.id`)。產生清單時，如果不想覆蓋，系統應幫忙統整與建新 List。

---

## 3. Jinja2 模板清單結構預告

前端畫面與資料將結合，必須建立以下檔案（繼承自 `base.html`）：

```text
app/templates/
├── base.html                     # 主框架 (Navbar, Flash Message, Footer)
├── auth/
│   ├── login.html
│   └── register.html
├── recipe/
│   ├── explore.html              # 探索公開/懶人食譜頁面
│   ├── detail.html               # 專屬食譜呈現頁
│   ├── new.html                  # 共用/新增表單
│   ├── edit.html                 # 編輯表單
│   └── cooking_mode.html         # (互動模式，可選擇不繼承 base 或者採用極簡 base)
├── shopping/
│   ├── index.html                # 我的購物清單一覽
│   └── detail.html               # 單一清單與採買檢核表
└── main/
    └── index.html                # 首頁儀表板 / 個人收藏
```
