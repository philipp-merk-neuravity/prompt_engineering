#!/bin/bash
PYTHON_INTERPRETER_PATH="$DEV_PATH/venv/bin/activate"
PYTHON_SCRIPT="$DEV_PATH/src/data_eval/tests_refinement_applied/create_plot.py"

source "$PYTHON_INTERPRETER_PATH"
python3 "$PYTHON_SCRIPT"
deactivate

