#!/bin/bash
PYTHON_INTERPRETER_PATH="$DEV_PATH/venv/bin/activate"

PATH_FOR_ITERATION_CREATION="$DEV_PATH/src/data_eval/reflection/create_results_for_iteration.py"
PATH_FOR_ITERATION_EVALUATION="$DEV_PATH/src/data_eval/reflection/get_pass_at_k_for_iterations.py"
PATH_FOR_DATA_AGGREGATION="$DEV_PATH/src/data_eval/reflection/keep_best/move_results.py"

source "$PYTHON_INTERPRETER_PATH"
python3 $PATH_FOR_ITERATION_CREATION
python3 $PATH_FOR_ITERATION_EVALUATION
python3 $PATH_FOR_DATA_AGGREGATION

deactivate
