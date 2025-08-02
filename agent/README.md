* RAG
* Model

cd script
python build_faiss_idx.py
python rag_main.py

### Challenges: 搜尋出來的結果很差?
原因
* 索引裡根本沒這筆
* 嵌入模型不對齊 (中/英文)