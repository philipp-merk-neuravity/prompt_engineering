#!/bin/bash

PYTHON_SCRIPT="/home/neuravity/dev/prompt_engineering/src/simple.py"
PYTHON_INTERPRETER_PATH="/home/neuravity/dev/prompt_engineering/venv/bin/activate"

source "$PYTHON_INTERPRETER_PATH"
python3 "$PYTHON_SCRIPT" --model="gpt-4-0125-preview" --prompt_type="zero_shot_cot" --benchmark_type="all" --chunk_size="86" --delay_seconds="10" --temperature="0.6"
deactivate
