import json
import matplotlib.pyplot as plt
from adjustText import adjust_text

path_for_data = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/simple_results_gpt4.json"

with open(path_for_data, 'r') as file:
    data = json.load(file)

# Prepare data for plotting
costs = [metrics['costs'] for metrics in data.values()]
accuracies = [metrics['accuracy'] for metrics in data.values()]
labels = list(data.keys())

# Plotting
fig, ax = plt.subplots()
points = ax.scatter(costs, accuracies)

texts = []
for i, label in enumerate(labels):
    texts.append(ax.text(costs[i], accuracies[i], label, ha='right', va='bottom', fontsize=9))

ax.grid(True, which='both', linestyle=':', color='gray', linewidth=0.5)
ax.set_xlabel('Kosten in Dollar')
ax.set_ylabel('Genauigkeit (pass@1)')

# Automatically adjust text labels without arrows
adjust_text(texts)

# Save
file_path = '/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/simple_cost_vs_accuracy_gpt4.png'
fig.savefig(file_path)