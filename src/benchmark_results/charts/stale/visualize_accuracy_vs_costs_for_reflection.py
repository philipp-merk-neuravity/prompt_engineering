import matplotlib.pyplot as plt
import json

path_for_data = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/reflection_results.json"

# Read the data
with open(path_for_data, 'r') as file:
    data = json.load(file)

# Prepare data for plotting
costs = []
accuracies = []
labels = []

for model_version, models in data.items():
    for model_name, metrics in models.items():
        costs.append(metrics['costs'])
        accuracies.append(metrics['accuracy'])
        labels.append(f"{model_version}, Code-Gen.: {model_name}")

# Plotting
fig, ax = plt.subplots()
ax.scatter(costs, accuracies)

# Determine the middle of the plot for label alignment
mid_point = sum(ax.get_xlim()) / 2

# Labeling the points with adjusted alignment
for i, label in enumerate(labels):
    ha = 'left' if costs[i] < mid_point else 'right'
    ax.text(costs[i], accuracies[i], label, ha=ha, va='bottom', fontsize=9)

ax.grid(True, which='both', linestyle=':', color='gray', linewidth=0.5)

ax.set_xlabel('Kosten in Dollar')
ax.set_ylabel('Genauigkeit')

plt.show()

# Save to file
file_path = '/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/reflection_cost_vs_accuracy.png'
fig.savefig(file_path)