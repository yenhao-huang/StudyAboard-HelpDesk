## webfile2json.py

將 URL 與內容儲存為 JSON 檔的小工具，可用於蒐集網頁資訊或筆記。

### How to Use
1. 執行 `streamlit run webfile2json.py`
2. 在網頁介面輸入：
   - URL
   - 內容
   - 選擇分類（例如 military、user_exp）
3. 按下「儲存到 JSON」後，系統會在對應資料夾中建立一個新的 JSON 檔，內容包含：
   - id
   - url
   - content
   - created_at
