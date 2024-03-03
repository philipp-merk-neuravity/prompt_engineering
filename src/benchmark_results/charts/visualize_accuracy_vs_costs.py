import json
import matplotlib.pyplot as plt

# Path to your JSON data
path_for_data = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/simple_results.json"

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
        labels.append(f"({model_name}, {model_version})")

# Plotting
fig, ax = plt.subplots()
ax.scatter(costs, accuracies)

# Get the limits of the axes to help determine label placement
x_lim = ax.get_xlim()
y_lim = ax.get_ylim()

# Determine the width of the plot
plot_width = x_lim[1] - x_lim[0]

for i, label in enumerate(labels):
    # Calculate the normalized position of the point within the plot
    normalized_x_position = (costs[i] - x_lim[0]) / plot_width

    # Choose alignment based on position to avoid overflow
    if normalized_x_position > 0.8:  # Adjust threshold as needed
        ha = 'right'
    else:
        ha = 'left'

    # Place text with adjusted alignment
    ax.text(costs[i], accuracies[i], label, ha=ha, va='bottom', fontsize=9)

# Add a grid with dotted lines
ax.grid(True, which='both', linestyle=':', color='gray', linewidth=0.5)

ax.set_xlabel('Kosten in Dollar')
ax.set_ylabel('Genauigkeit')

# Save to file
file_path = '/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/simple_cost_vs_accuracy.png'
fig.savefig(file_path)
