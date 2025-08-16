cd ../script
python build_faiss_idx.py \
--model sentence-transformers/all-MiniLM-L6-v2 \
--faiss_idx_path ../index/sentencetransformer_faiss
python evaluate.py \
--setting sentencetf 
