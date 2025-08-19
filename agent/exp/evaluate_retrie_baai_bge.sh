cd ../script
python build_faiss_idx.py \
--model BAAI/bge-m3 \
--faiss_idx_path ../index/baai_bge_m3_faiss
python evaluate.py \
--setting baai_bge_m3 \
--eval_type retrieval