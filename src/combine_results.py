from utils.storage import load_benchmark_results
import json

path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/simple/0.6/zero_shot_cot/gpt-4-0125-preview"

combined_results = []
for i in range(10):
    current_path = path + f"/{i}/{i}.jsonl"
    print(current_path)
    combined_results.extend(load_benchmark_results(current_path))

with open(f"{path}/combined_results.jsonl", 'w') as file:
    for result in combined_results:
        file.write(json.dumps(result) + '\n') 