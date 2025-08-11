* RAG
* Model

## How to Run
0. data preprocess

cd script/data_preprocess
python label_uuid.py # 增加識別碼

1. 建立 faiss index
cd script
python build_faiss_idx.py

2. 執行 RAG
python rag_main.py

### Challenges: 搜尋出來的結果很差?
原因
* 索引裡根本沒這筆
* 嵌入模型不對齊 (中/英文)