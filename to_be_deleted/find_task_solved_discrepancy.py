from src.utils.storage import load_benchmark_results

path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/reflection/standard/gpt-3/9/9.jsonl_results.jsonl"
result_data = load_benchmark_results(path)

for item in result_data:
    if item["is_solved"] != item["passed"]:
        print(item["task_id"])