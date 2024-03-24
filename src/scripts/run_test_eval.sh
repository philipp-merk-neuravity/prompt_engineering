#!/bin/bash

PYTHON_SCRIPT="$DEV_PATH/src/eval_tests.py"
TEST_CASES="$DEV_PATH/src/benchmark_results/test_cases/0.2/io/gpt-3.5-turbo-0125/with_refinement/gpt-3.5-turbo-0125/3/3.jsonl"
PYTHON_INTERPRETER_PATH="$DEV_PATH/venv/bin/activate"

source "$PYTHON_INTERPRETER_PATH"
python3 "$PYTHON_SCRIPT" --path_for_test_cases="$TEST_CASES"
deactivate
