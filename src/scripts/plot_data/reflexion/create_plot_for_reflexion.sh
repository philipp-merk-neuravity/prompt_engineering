#!/bin/bash
PYTHON_INTERPRETER_PATH="$DEV_PATH/venv/bin/activate"
PATH_FOR_PLOT_CREATION="$DEV_PATH/src/data_eval/reflection/keep_best/create_plot.py"

source "$PYTHON_INTERPRETER_PATH"
python3 $PATH_FOR_PLOT_CREATION

deactivate