#!/bin/bash

PYTHON_SCRIPT="/home/neuravity/dev/prompt_engineering/src/eval_tests.py"
TEST_CASES="/home/neuravity/dev/prompt_engineering/src/benchmark_results/test_cases/few_shot/gpt-3.5-turbo-0125/with_refinement/gpt-3.5-turbo-0125/6/6.jsonl"
PYTHON_INTERPRETER_PATH="/home/neuravity/dev/prompt_engineering/venv/bin/activate"

source "$PYTHON_INTERPRETER_PATH"
python3 "$PYTHON_SCRIPT" --path_for_test_cases="$TEST_CASES"
deactivate
