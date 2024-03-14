#!/bin/bash

PYTHON_SCRIPT="/home/neuravity/dev/prompt_engineering/src/human_eval/human_eval/evaluate_functional_correctness.py"
BENCHMARK_RESULTS="/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/simple/0.6/io/gpt-4-0125-preview/init_file/combined_results.jsonl"
PROBLEM_FILE="/home/neuravity/dev/prompt_engineering/src/human_eval/data/HumanEval.jsonl"
PYTHON_INTERPRETER_PATH="/home/neuravity/dev/prompt_engineering/venv/bin/activate"

source "$PYTHON_INTERPRETER_PATH"
python3 "$PYTHON_SCRIPT" "$BENCHMARK_RESULTS" --problem_file="$PROBLEM_FILE" --k="1"
deactivate