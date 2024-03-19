#!/bin/bash

PYTHON_SCRIPT="/home/neuravity/dev/prompt_engineering/src/eval_tests.py"
TEST_CASES="/home/neuravity/dev/prompt_engineering/src/benchmark_results/test_cases/0.2/zero_shot_cot/gpt-4-0125-preview/with_refinement/gpt-4-0125-preview/2/2.jsonl"
PYTHON_INTERPRETER_PATH="/home/neuravity/dev/prompt_engineering/venv/bin/activate"

source "$PYTHON_INTERPRETER_PATH"
python3 "$PYTHON_SCRIPT" --path_for_test_cases="$TEST_CASES"
deactivate
