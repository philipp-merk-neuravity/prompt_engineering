import json

path_for_data = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_tests/test_results_with_costs.json"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_tests"

with open(path_for_data, 'r') as file:
    data = json.load(file)

for item in data: 
    efficiency = item["accuracy"] / item["total_cost"]
    item["efficiency"] = efficiency

with open(save_path + '/test_results_with_efficiency.json', 'w') as file:
    json.dump(data, file, indent=4)

