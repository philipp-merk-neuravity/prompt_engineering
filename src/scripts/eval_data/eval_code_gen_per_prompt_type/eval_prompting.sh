#!/bin/bash
PYTHON_INTERPRETER_PATH="$DEV_PATH/venv/bin/activate"

source "$PYTHON_INTERPRETER_PATH"

python3 "$DEV_PATH/src/combine_results.py" --path "$DEV_PATH/src/benchmark_results/code_gen/simple/0.8/io/gpt-3.5-turbo-0125" 
python3 "$DEV_PATH/src/combine_results.py" --path "$DEV_PATH/src/benchmark_results/code_gen/simple/0.8/scot/gpt-3.5-turbo-0125" 
python3 "$DEV_PATH/src/combine_results.py" --path "$DEV_PATH/src/benchmark_results/code_gen/simple/0.8/synth_few_shot_split/gpt-3.5-turbo-0125" 
python3 "$DEV_PATH/src/combine_results.py" --path "$DEV_PATH/src/benchmark_results/code_gen/simple/0.8/zero_shot_cot/gpt-3.5-turbo-0125" 
python3 "$DEV_PATH/src/combine_results.py" --path "$DEV_PATH/src/benchmark_results/code_gen/simple/0.6/io/gpt-4-0125-preview" 
python3 "$DEV_PATH/src/combine_results.py" --path "$DEV_PATH/src/benchmark_results/code_gen/simple/0.6/scot/gpt-4-0125-preview" 
python3 "$DEV_PATH/src/combine_results.py" --path "$DEV_PATH/src/benchmark_results/code_gen/simple/0.6/synth_few_shot_split/gpt-4-0125-preview" 
python3 "$DEV_PATH/src/combine_results.py" --path "$DEV_PATH/src/benchmark_results/code_gen/simple/0.6/zero_shot_cot/gpt-4-0125-preview" 

python3 "$DEV_PATH/src/data_eval/simple/get_pass_at_k.py" --mapping_path="$DEV_PATH/src/scripts/eval_data/eval_code_gen_per_prompt_type/mapping_for_prompting.json"
python3 "$DEV_PATH/src/data_eval/simple/combine_pass_at_k.py" --mapping_path="$DEV_PATH/src/scripts/eval_data/eval_code_gen_per_prompt_type/mapping_for_prompting.json" --save_path="$DEV_PATH/src/benchmark_results/results/data/eval_prompt_method/combined_results_prompt_method.jsonl"

deactivate
