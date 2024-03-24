PYTHON_SCRIPT="$DEV_PATH/src/data_eval/temperature/create_plot_temp.py"
PYTHON_INTERPRETER_PATH="$DEV_PATH/venv/bin/activate"

source "$PYTHON_INTERPRETER_PATH"
python3 $PYTHON_SCRIPT
deactivate