#!/bin/bash

PYTHON_SCRIPT="$DEV_PATH/src/gen_tests.py"
PYTHON_INTERPRETER_PATH="$DEV_PATH/venv/bin/activate"

# --chunk_size: If a rate limit is hit, lower the chunk size. Default is 50.
# --model_for_refinement: Can be either unset as "" or: gpt-3.5-turbo-0125, gpt-4-0125-preview

source "$PYTHON_INTERPRETER_PATH"
python3 "$PYTHON_SCRIPT" --model "gpt-4-0125-preview" --prompt_type "zero_shot_cot" --chunk_size "50" --model_for_refinement "gpt-4-0125-preview" --temperature "0.2"
deactivate