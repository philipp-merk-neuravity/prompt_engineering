#!/bin/bash

PYTHON_SCRIPT="/home/neuravity/dev/prompt_engineering/src/gen_tests.py"
PYTHON_INTERPRETER_PATH="/home/neuravity/dev/prompt_engineering/venv/bin/activate"

# --model: gpt-3.5-turbo-0125, gpt-4-0125-preview
# --prompt_type: io, zero_shot_cot, few_shot
# --chunk_size: If a rate limit is hit, lower the chunk size. Default is 50.
# --model_for_refinement: Can be either unset as "" or: gpt-3.5-turbo-0125, gpt-4-0125-preview

source "$PYTHON_INTERPRETER_PATH"
python3 "$PYTHON_SCRIPT" --model "gpt-4" --prompt_type "few_shot" --chunk_size "50" --model_for_refinement "" --temperature "0.2"
deactivate