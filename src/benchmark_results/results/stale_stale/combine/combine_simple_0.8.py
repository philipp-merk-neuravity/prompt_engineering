import json
path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/simple/0.8/zero_shot_cot/gpt-3.5-turbo-0125"
current_model = "gpt-3.5-turbo"
method = "zero_shot_cot"

path_for_costs = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/costs.json"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_prompt_method/0.8/gpt_3.5"

with open(path_for_costs, 'r') as file:
    costs = json.load(file)[current_model]

combined_results = []

for i in range(5):
    current_path = path + f"/{i}/combined_results.jsonl_stats.json"
    with open(current_path, 'r') as file:
        for line in file:
            result = json.loads(line.strip())
            result["cost"] = {
                "input": costs["input"] * result["prompt_tokens"] / 1000000,
                "output": costs["output"] * result["completion_tokens"] / 1000000,
                "total": (costs["input"] * result["prompt_tokens"] / 1000000) + (costs["output"] * result["completion_tokens"] / 1000000)
            }
            combined_results.append(result)

# save the combined results
with open(f"{save_path}/{method}_results.jsonl", 'w') as file:
    for result in combined_results:
        file.write(json.dumps(result) + '\n')