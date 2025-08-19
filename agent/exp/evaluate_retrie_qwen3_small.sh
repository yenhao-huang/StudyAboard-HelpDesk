cd ../script
python build_faiss_idx.py \
--model Qwen/Qwen3-Embedding-0.6B \
--faiss_idx_path ../index/qwen3_faiss_small
python evaluate.py \
--setting qwen3_small \
--eval_type retrieval