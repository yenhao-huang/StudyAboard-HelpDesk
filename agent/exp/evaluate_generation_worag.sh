cd ../script
python evaluate.py \
--benchmark_dir ../data/eval/qa \
--setting alibaba_worag \
--output_path ../results/qa/evaluation_results_worag.csv
cd eval
python count_ncorrect.py \
--input_file evaluation_results_worag.csv