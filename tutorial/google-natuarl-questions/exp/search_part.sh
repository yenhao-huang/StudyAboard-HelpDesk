cd ..
python script/build_faiss_idx.py --doc_path data/nq_passages_1000.json --faiss_idx_path index/nq_langchain_faiss_1000
python script/search_faiss_idx.py --faiss_idx_path index/nq_langchain_faiss_1000