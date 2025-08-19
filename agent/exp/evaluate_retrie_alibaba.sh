cd ../script
python build_faiss_idx.py \
--model Alibaba-NLP/gte-multilingual-base \
--faiss_idx_path ../index/alibaba_faiss
python evaluate.py \
--setting alibaba \
--eval_type retrieval