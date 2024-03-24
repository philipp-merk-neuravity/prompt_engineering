#!/bin/bash
PYTHON_SCRIPT="$DEV_PATH/src/simple.py"
PYTHON_INTERPRETER_PATH="$DEV_PATH/venv/bin/activate"

source "$PYTHON_INTERPRETER_PATH"
python3 "$PYTHON_SCRIPT" --model="gpt-4-0125-preview" --prompt_type="io" --benchmark_type="all" --chunk_size="86" --delay_seconds="10" --temperature="0.6"
deactivate
