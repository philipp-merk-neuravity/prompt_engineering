#!/bin/bash
PYTHON_INTERPRETER_PATH="$DEV_PATH/venv/bin/activate"

source "$PYTHON_INTERPRETER_PATH"
python3 "$DEV_PATH/src/simple_reflection.py" \
  --model_for_reflection "gpt-3.5-turbo-0125" \
  --model_for_refinement "gpt-3.5-turbo-0125" \
  --prompt_for_reflection "simple" \
  --prompt_for_refinement "simple" \
  --max_iterations "10" \
  --benchmark_type "all" \
  --chunk_size "57" \
  --tests_path "$DEV_PATH/src/human_eval/data/ExtractedTests.json" \
  --file_path_for_init "$DEV_PATH/src/benchmark_results/code_gen/simple/0.8/io/gpt-3.5-turbo-0125/init_file/combined_results.jsonl" \
  --temp_for_reflection "0.8" \
  --temp_for_refinement "0.8" \
  --test_type "predefined" \

deactivate
