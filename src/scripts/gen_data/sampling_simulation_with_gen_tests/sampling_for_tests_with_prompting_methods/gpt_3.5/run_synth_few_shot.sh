#!/bin/bash
PYTHON_SCRIPT="$DEV_PATH/src/simulate_sampling_with_gen_tests.py"
PYTHON_INTERPRETER_PATH="$DEV_PATH/venv/bin/activate"

source "$PYTHON_INTERPRETER_PATH"
python3 "$PYTHON_SCRIPT" --method="io" --model="gpt-3.5-turbo-0125" --temperature="0.8" --test_type="tests_3.5_synth_few_shot" --test_path="synth_few_shot/gpt-3.5-turbo-0125/without_refinement/1/1.jsonl"
deactivate
