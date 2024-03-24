#!/bin/bash

PYTHON_SCRIPT="$DEV_PATH/src/human_eval/human_eval/evaluate_functional_correctness.py"
BENCHMARK_RESULTS="$DEV_PATH/src/benchmark_results/code_gen/simple/0.6/io/gpt-4-0125-preview/combined_results.jsonl"
PROBLEM_FILE="$DEV_PATH/src/human_eval/data/HumanEval.jsonl"
PYTHON_INTERPRETER_PATH="$DEV_PATH/venv/bin/activate"

source "$PYTHON_INTERPRETER_PATH"
python3 "$PYTHON_SCRIPT" "$BENCHMARK_RESULTS" --problem_file="$PROBLEM_FILE" --k="10"
deactivate

#!/bin/bash
PYTHON_INTERPRETER_PATH="$DEV_PATH/venv/bin/activate"

source "$PYTHON_INTERPRETER_PATH"

deactivate