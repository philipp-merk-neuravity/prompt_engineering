import json

data_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_prompt_method/0.8/gpt_4/results_simple_0.8_gpt_4.jsonl"

data = {}

with open(data_path, 'r') as file:
    data = json.load(file)

# Initialize variables to find the min and max for accuracy and cost
min_accuracy = float('inf')
max_accuracy = float('-inf')
min_cost = float('inf')
max_cost = float('-inf')

# Find the overall min and max for accuracy and cost
for method in data.values():
    for entry in method:
        accuracy = list(entry["accuracy"].values())[0]
        cost = entry["cost"]["total"]
        if accuracy < min_accuracy:
            min_accuracy = accuracy
        if accuracy > max_accuracy:
            max_accuracy = accuracy
        if cost < min_cost:
            min_cost = cost
        if cost > max_cost:
            max_cost = cost

# Function to apply min-max normalization
def minmax_normalize(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value)


def run_utility_analysis(accuracy, cost, a, c):
    return accuracy/cost

# Apply min-max normalization and calculate utility for each row
normalized_data = {}

a = 0.9
c = 0.1

for method_name, method in data.items():
    normalized_entries = []
    for entry in method:
        accuracy_key = list(entry["accuracy"].keys())[0]
        accuracy_value = list(entry["accuracy"].values())[0]
        # Extract sample size from the accuracy key
        sample_size = int(accuracy_key.split('@')[1])
        normalized_accuracy = minmax_normalize(accuracy_value, min_accuracy, max_accuracy)
        normalized_cost = minmax_normalize(entry["cost"]["total"], min_cost, max_cost)
        utility_score = run_utility_analysis(accuracy_value, entry["cost"]["total"], a, c)
        normalized_entries.append({
            "sample_size": sample_size,
            "normalized_accuracy": normalized_accuracy,
            "normalized_cost": normalized_cost,
            "utility_score": utility_score,
            "accuracy": accuracy_value,
            "total_cost": entry["cost"]["total"],
        })
    normalized_data[method_name] = normalized_entries

# Save the normalized data with utility scores
with open("/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_prompt_method/0.2/gpt_4/normalized_data_with_utility_gpt4.json", 'w') as file:
    json.dump(normalized_data, file, indent=4)