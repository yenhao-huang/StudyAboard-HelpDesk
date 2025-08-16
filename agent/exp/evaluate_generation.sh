cd ../script
python evaluate.py \
--benchmark_dir ../data/eval/qa \
--output_path ../results/qa/evaluation_results.csv \
--openrouter_setting 1
cd eval
python count_ncorrect.py \
--input_file evaluation_results.csv