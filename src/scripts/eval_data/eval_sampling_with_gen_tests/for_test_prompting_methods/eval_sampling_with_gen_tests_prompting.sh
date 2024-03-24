#!/bin/bash
PYTHON_INTERPRETER_PATH="$DEV_PATH/venv/bin/activate"
PATH_FOR_COMBINATION="$DEV_PATH/src/data_eval/tests_with_methods_applied/combine_results.py"

source "$PYTHON_INTERPRETER_PATH"
python3 "$PATH_FOR_COMBINATION"

deactivate