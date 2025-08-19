cd ../script
python build_faiss_idx.py \
--model BAAI/bge-large-zh-v1.5 \
--faiss_idx_path ../index/baai_faiss
python evaluate.py \
--setting baai \
--eval_type retrieval