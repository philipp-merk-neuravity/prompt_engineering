#!/bin/bash
PYTHON_INTERPRETER_PATH="$DEV_PATH/venv/bin/activate"

source "$PYTHON_INTERPRETER_PATH"

python3 "$DEV_PATH/src/combine_results.py" --path "$DEV_PATH/src/benchmark_results/code_gen/simple/0.2/io/gpt-3.5-turbo-0125" 
python3 "$DEV_PATH/src/combine_results.py" --path "$DEV_PATH/src/benchmark_results/code_gen/simple/0.4/io/gpt-3.5-turbo-0125" 
python3 "$DEV_PATH/src/combine_results.py" --path "$DEV_PATH/src/benchmark_results/code_gen/simple/0.6/io/gpt-3.5-turbo-0125" 
python3 "$DEV_PATH/src/combine_results.py" --path "$DEV_PATH/src/benchmark_results/code_gen/simple/0.8/io/gpt-3.5-turbo-0125" 

python3 "$DEV_PATH/src/data_eval/simple/get_pass_at_k.py" --mapping_path="$DEV_PATH/src/scripts/eval_data/eval_temp/mapping_for_temp.json"
python3 "$DEV_PATH/src/data_eval/simple/combine_pass_at_k.py" --mapping_path="$DEV_PATH/src/scripts/eval_data/eval_temp/mapping_for_temp.json" --save_path="$DEV_PATH/src/benchmark_results/results/data/temperature/combined_results_temp.jsonl"

deactivate