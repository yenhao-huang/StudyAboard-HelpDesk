# 設定 Google Cloud 以列出資料夾內所有檔案

目標：取得指定 Google Drive 資料夾中所有檔案的：

* 📄 檔名（name）
* 🆔 檔案 ID（file ID）
* 📦 MIME type
* 🔗 可下載連結（`gdown` 或 `export=download`）

---

## 1. 安裝必要套件

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

---

## 2. 建立 Google Cloud 專案與 OAuth 憑證

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)

2. 建立或選擇一個專案

3. 點選側邊選單：

   ```
   API 和服務 → OAuth 同意畫面
   ```

4. 選擇「**外部**」應用程式（一般選這個）

5. 填寫以下資訊：

   * 應用程式名稱
   * 支援電子郵件
   * 開發人員聯絡電子郵件
   * （選填）LOGO、網站網址等

6. 點選「**儲存並繼續**」直到完成

---

## 3. 啟用 Google Drive API 並下載憑證

1. 回到專案首頁 → 點選：

   ```
   API 與服務 → 資源庫
   ```

2. 搜尋並啟用：**Google Drive API**

3. 建立憑證：

   * 類型選擇：**桌面應用程式**
   * 建立後，下載 `credentials.json`

---

## 4. 憑證存放建議目錄

將憑證放入 `secrets/` 子資料夾（便於安全管理）：

```
secrets/
├── credentials.json   ← 放這
```

⚠️ 建議將 `secrets/` 加入 `.gitignore` 避免誤傳到版本控制系統。

---

## 5. 新增自己的 Gmail 為「測試人員」

1. 回到 [Google Cloud Console](https://console.cloud.google.com/)

2. 選擇你的專案（例如 `RAG-Chatbot`）

3. 點選側邊選單：

   ```
   API 和服務 → OAuth 同意畫面
   ```

4. 捲動到底部「**測試人員**」區塊

5. 新增你的 Gmail 帳號（例如：`blackpig22017@gmail.com`）

6. 點選「儲存」
