cd ../script
python build_faiss_idx.py \
--model TencentBAC/Conan-embedding-v1 \
--faiss_idx_path ../index/tencent_conan_faiss
python evaluate.py \
--setting tencent_conan \
--eval_type retrieval
