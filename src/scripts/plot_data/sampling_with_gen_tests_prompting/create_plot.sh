#!/bin/bash

PYTHON_INTERPRETER_PATH="$DEV_PATH/venv/bin/activate"
FILE_PATH="$DEV_PATH/src/data_eval/tests_with_methods_applied/create_plot.py"

source "$PYTHON_INTERPRETER_PATH"
python3 $FILE_PATH

deactivate