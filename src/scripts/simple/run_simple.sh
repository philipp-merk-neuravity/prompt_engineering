#!/bin/bash

PYTHON_SCRIPT="/home/neuravity/dev/prompt_engineering/src/simple.py"
PYTHON_INTERPRETER_PATH="/home/neuravity/dev/prompt_engineering/venv/bin/activate"

source "$PYTHON_INTERPRETER_PATH"
python3 "$PYTHON_SCRIPT" --model="gpt-3.5-turbo-0125" --prompt_type="zero_shot_cot" --benchmark_type="all" --chunk_size="180" --delay_seconds="10" --temperature="0.8"
deactivate
