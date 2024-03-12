import json
import matplotlib.pyplot as plt

save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/img/simple_0.2/gpt4"

# Load data from a JSON file
file_path = '/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_prompt_method/0.2/gpt_4/normalized_data_with_utility_gpt4.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Extract method names and corresponding values for utility score, accuracy, and total cost
methods = list(data.keys())
utility_scores = [data[method][0]["utility_score"] for method in methods]
accuracies = [data[method][0]["accuracy"] for method in methods]
total_costs = [data[method][0]["total_cost"] for method in methods]

# Utility Scores Plot
plt.figure(figsize=(10, 5))
plt.bar(methods, utility_scores, color=['orange', 'red', 'blue', 'green'])
plt.title('Utility Scores by Method')
plt.ylabel('Utility Score')
plt.savefig(save_path + '/utility_scores_by_method.png')
plt.close()

# Accuracies Plot
plt.figure(figsize=(10, 5))
plt.bar(methods, accuracies, color=['orange', 'red', 'blue', 'green'])
plt.title('Accuracies by Method')
plt.ylabel('Accuracy')
plt.savefig(save_path + '/accuracies_by_method.png')
plt.close()

# Total Costs Plot
plt.figure(figsize=(10, 5))
plt.bar(methods, total_costs, color=['orange', 'red', 'blue', 'green'])
plt.title('Total Costs by Method')
plt.ylabel('Cost in Dollars')
plt.savefig(save_path + '/total_costs_by_method.png')
plt.close()
