import json

path_for_data = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_prompt_method/0.8/gpt_3.5/results_simple_0.8_gpt_3.5.json"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_prompt_method/0.8/gpt_3.5"

with open(path_for_data, 'r') as file:
    data = json.load(file)

for method, results in data.items():
    for result in results:
        accuracy = next(iter(result['accuracy'].values()))  # Get the first (and only) accuracy value
        total_cost = result['cost']['total']
        efficiency = accuracy / total_cost
        result['efficiency'] = efficiency

with open(save_path + '/results_simple_0.8_gpt_3.5_with_efficiency.json', 'w') as file:
    json.dump(data, file, indent=4)