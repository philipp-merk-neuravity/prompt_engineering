import json
import matplotlib.pyplot as plt

save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/img/simple_0.2/gpt3.5"

# Load data from a JSON file
file_path = '/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_prompt_method/0.2/gpt_3.5/combined_results_with_benefit.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Extract method names and corresponding values for utility score, accuracy, and total cost
methods = list(data.keys())
utility_scores = [data[method][0]["cost_efficiency_ratio"] for method in methods]
accuracies = [data[method][0]["accuracy"]["pass@1"] for method in methods]
total_costs = [data[method][0]["cost"]["total"] for method in methods]

# Utility Scores Plot
plt.figure(figsize=(10, 5))
plt.bar(methods, utility_scores, color=['orange', 'red', 'blue', 'green'])
plt.ylabel('Genauigkeit pro Kosten')
plt.savefig(save_path + '/utility_scores_by_method.png')
plt.close()

# Accuracies Plot
plt.figure(figsize=(10, 5))
plt.bar(methods, accuracies, color=['orange', 'red', 'blue', 'green'])
plt.ylabel('Genauigkeit')
plt.savefig(save_path + '/accuracies_by_method.png')
plt.close()

# Total Costs Plot
plt.figure(figsize=(10, 5))
plt.bar(methods, total_costs, color=['orange', 'red', 'blue', 'green'])
plt.ylabel('Kosten in Dollar')
plt.savefig(save_path + '/total_costs_by_method.png')
plt.close()
