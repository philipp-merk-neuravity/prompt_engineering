
#!/bin/bash
PYTHON_INTERPRETER_PATH="$DEV_PATH/venv/bin/activate"
SAVE_PATH="$DEV_PATH/src/benchmark_results/results/data/eval_tests_refinement"

source "$PYTHON_INTERPRETER_PATH"
python3 "$DEV_PATH/src/eval_multiple_tests.py" --mapping_path="$DEV_PATH/src/scripts/eval_data/eval_tests/eval_tests_with_removal/mapping.json" --save_path="$SAVE_PATH"
deactivate
