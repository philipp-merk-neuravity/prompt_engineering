  # --model_for_reflection "gpt-3.5-turbo-0125" | "gpt-4-0125-preview" \
  # --model_for_refinement "gpt-3.5-turbo-0125" | "gpt-4-0125-preview" \
  # --prompt_for_reflection "simple" \
  # --prompt_for_refinement "simple" \
  # --max_iterations "10" \
  # --benchmark_type "all" \
  # --chunk_size "57" \
  # --tests_path "/home/neuravity/dev/prompt_engineering/src/human_eval/data/ExtractedTests.json" \
  # --file_path_for_init "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/simple/0.8/io/gpt-3.5-turbo-0125/init_file/combined_results.jsonl" | "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/simple/0.6/io/gpt-4-0125-preview/init_file/combined_results.jsonl" \
  # --temp_for_reflection "0.8" | "0.6" \
  # --temp_for_refinement "0.8" | "0.6" \
  # --test_type "predefined" \

python3 "/home/neuravity/dev/prompt_engineering/src/simple_reflection.py" \
  --model_for_reflection "gpt-3.5-turbo-0125" \
  --model_for_refinement "gpt-3.5-turbo-0125" \
  --prompt_for_reflection "simple" \
  --prompt_for_refinement "simple" \
  --max_iterations "10" \
  --benchmark_type "all" \
  --chunk_size "57" \
  --tests_path "/home/neuravity/dev/prompt_engineering/src/human_eval/data/ExtractedTests.json" \
  --file_path_for_init "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/simple/0.8/io/gpt-3.5-turbo-0125/init_file/combined_results.jsonl" \
  --temp_for_reflection "0.8" \
  --temp_for_refinement "0.8" \
  --test_type "predefined" \
