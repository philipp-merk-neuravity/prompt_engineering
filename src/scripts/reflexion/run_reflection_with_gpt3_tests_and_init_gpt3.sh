python3 "/home/neuravity/dev/prompt_engineering/src/reflection.py" \
  --model_for_reflection "gpt-3.5-turbo-0125" \
  --model_for_refinement "gpt-3.5-turbo-0125" \
  --prompt_for_reflection "reflexion_without_few_shot" \
  --prompt_for_refinement "reflexion_without_few_shot" \
  --max_iterations "4" \
  --benchmark_type "all" \
  --chunk_size "57" \
  --tests_path "/home/neuravity/dev/prompt_engineering/src/benchmark_results/test_cases/io/gpt-3.5-turbo-0125/2/2.jsonl" \
  --file_path_for_init "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/simple/io/gpt-3.5-turbo-0125/4/4.jsonl" \
  --test_case_type "with_gpt-3.5-turbo_test_cases" \