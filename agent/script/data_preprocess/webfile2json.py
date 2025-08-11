# save_note_ui.py
import streamlit as st
import json
import os
import uuid
import datetime as dt

BASE_DIR = "../../data/docs"
OUT_DIR_OPTIONS = {
    "military": os.path.join(BASE_DIR, "military"),
    "user_exp": os.path.join(BASE_DIR, "user_exp"),
}

st.title("📄 Save URL & Content to JSON")

# 選擇輸出分類
category = st.selectbox("選擇分類", list(OUT_DIR_OPTIONS.keys()))
OUT_DIR = OUT_DIR_OPTIONS[category]

# 輸入欄位
url = st.text_input("輸入 URL", placeholder="https://example.com")
content = st.text_area("輸入內容", placeholder="在這裡輸入你的筆記或內容...")

if st.button("💾 儲存到 JSON"):
    if not url.strip():
        st.error("❌ 請輸入 URL")
    elif not content.strip():
        st.error("❌ 請輸入內容")
    else:
        record = {
            "id": str(uuid.uuid4()),
            "url": url.strip(),
            "content": content.strip(),
            "created_at": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        }

        os.makedirs(OUT_DIR, exist_ok=True)
        OUT_FILE = os.path.join(OUT_DIR, f"{uuid.uuid4()}.json")

        # 檔案直接存單筆記錄
        with open(OUT_FILE, "w", encoding="utf-8") as f:
            json.dump([record], f, ensure_ascii=False, indent=2)

        st.success(f"✅ 已儲存到 {OUT_FILE}")
        st.json(record)
