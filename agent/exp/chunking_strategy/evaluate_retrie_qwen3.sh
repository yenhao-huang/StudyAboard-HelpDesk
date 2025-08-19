#!/bin/bash
set -e

cd ../../script

# 全域參數
EMB_MODEL="Qwen/Qwen3-Embedding-0.6B"
CHUNK_SIZES=(256 1024 4096)

for CHUNK_SIZE in "${CHUNK_SIZES[@]}"; do
  echo "=== Running with EMB_MODEL=${EMB_MODEL}, CHUNK_SIZE=${CHUNK_SIZE} ==="

  python build_faiss_idx.py \
    --model ${EMB_MODEL} \
    --faiss_idx_path ../index/${EMB_MODEL}_faiss_${CHUNK_SIZE} \
    --chunk_size ${CHUNK_SIZE}

  python update_config.py \
    --emb_model ${EMB_MODEL} \
    --faiss_idx_path ../index/${EMB_MODEL}_faiss_${CHUNK_SIZE} \
    --k 5 \
    --chatbot_model moonshotai/kimi-k2:free \
    --judge_model google/gemma-3-27b-it:free

  python evaluate.py \
    --setting custom \
    --eval_type retrieval \
    --output_path ../results/retrieval/chunk_size/${EMB_MODEL}_${CHUNK_SIZE}.csv
done