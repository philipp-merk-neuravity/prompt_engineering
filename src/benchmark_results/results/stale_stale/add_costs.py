import json

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

file_path_for_costs = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/costs.json"
file_path_for_performance = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/simple_results.json"

def calculate_costs(data_performance, data_costs):
    for version, methods in data_performance.items():
        for method, stats in methods.items():
            input_cost = float(data_costs[version]["input"])
            output_cost = float(data_costs[version]["output"])
            input_costs = stats["prompt_tokens"] * input_cost / 1000000
            output_costs = stats["completion_tokens"] * output_cost / 1000000
            total_cost = input_costs + output_costs
            stats["costs"] = total_cost
    return data_performance

data_costs = read_json_file(file_path_for_costs)
data_performance = read_json_file(file_path_for_performance)
updated_data1 = calculate_costs(data_performance, data_costs)

with open(file_path_for_performance, 'w') as file:
    json.dump(updated_data1, file, indent=4)