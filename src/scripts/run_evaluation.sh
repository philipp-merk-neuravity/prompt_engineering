#!/bin/bash

PYTHON_SCRIPT="/home/neuravity/dev/prompt_engineering/src/human_eval/human_eval/evaluate_functional_correctness.py"
BENCHMARK_RESULTS="/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/reflection/simple_simple/0.8_0.8/gpt-3.5-turbo-0125/use_next/gpt_3.5-turbo-0125_gpt-4-0125-preview/combined_results.jsonl"
PROBLEM_FILE="/home/neuravity/dev/prompt_engineering/src/human_eval/data/HumanEval.jsonl"
PYTHON_INTERPRETER_PATH="/home/neuravity/dev/prompt_engineering/venv/bin/activate"

source "$PYTHON_INTERPRETER_PATH"
python3 "$PYTHON_SCRIPT" "$BENCHMARK_RESULTS" --problem_file="$PROBLEM_FILE" --k="1"
deactivate