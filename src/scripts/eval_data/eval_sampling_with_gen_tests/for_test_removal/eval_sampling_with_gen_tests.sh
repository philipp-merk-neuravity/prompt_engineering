#!/bin/bash
PYTHON_INTERPRETER_PATH="$DEV_PATH/venv/bin/activate"
PATH_FOR_COMBINATION="$DEV_PATH/src/data_eval/tests_refinement_applied/combine.py"

source "$PYTHON_INTERPRETER_PATH"
python3 "$PATH_FOR_COMBINATION"
deactivate