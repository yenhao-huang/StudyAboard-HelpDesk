cd ../script
python build_faiss_idx.py \
--model Qwen/Qwen3-Embedding-8B \
--faiss_idx_path ../index/qwen3_faiss
python evaluate.py \
--setting qwen3 \
--eval_type retrieval