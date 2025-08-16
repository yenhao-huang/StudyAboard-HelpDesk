cd ../script

settings=(mistral deepseek)

for setting in "${settings[@]}"
do
    echo "Evaluating $setting..."
    python evaluate.py \
        --benchmark_dir ../data/eval/qa \
        --setting $setting \
        --output_path ../results/qa/evaluation_results_${setting}.csv \
        --openrouter_setting 1
done

cd eval

for setting in "${settings[@]}"
do
    python count_ncorrect.py \
        --input_file evaluation_results_${setting}.csv
done
