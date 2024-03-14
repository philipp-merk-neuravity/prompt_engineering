path_for_data = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_prompt_method/0.2/gpt_3.5/combined_results_for_gpt3.json"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_prompt_method/0.2/gpt_3.5"

import json
import matplotlib.pyplot as plt

# Load data from a JSON file

with open(path_for_data, 'r') as file:
    data = json.load(file)

# Calculating cost efficiency ratio (accuracy per unit cost)
for method in data:
    for result in data[method]:
        accuracy = result['accuracy']['pass@1']
        total_cost = result['cost']['total']
        cost_efficiency_ratio = accuracy / total_cost
        result['cost_efficiency_ratio'] = cost_efficiency_ratio


with open(save_path + '/combined_results_with_benefit.json', 'w') as file:
    json.dump(data, file, indent=4)