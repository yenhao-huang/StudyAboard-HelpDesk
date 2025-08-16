#!/bin/bash

cd ../script

settings=(mistral_worag deepseek_worag)

# 跑 evaluate
for setting in "${settings[@]}"
do
    echo "Evaluating $setting..."
    python evaluate.py \
        --benchmark_dir ../data/eval/qa \
        --setting "$setting" \
        --output_path ../results/qa/evaluation_results_${setting}.csv
done

cd eval

# 跑 count_ncorrect
for setting in "${settings[@]}"
do
    python count_ncorrect.py \
        --input_file evaluation_results_${setting}.csv
done
