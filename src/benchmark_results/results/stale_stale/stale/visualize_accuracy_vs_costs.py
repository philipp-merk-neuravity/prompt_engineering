# import json
# import matplotlib.pyplot as plt

# # Path to your JSON data
# path_for_data = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/simple_results_gpt4.json"

# # Read the data
# with open(path_for_data, 'r') as file:
#     data = json.load(file)

# # Prepare data for plotting
# costs = []
# accuracies = []
# labels = []

# for model_version, models in data.items():
#     for model_name, metrics in models.items():
#         costs.append(metrics['costs'])
#         accuracies.append(metrics['accuracy'])
#         labels.append(f"({model_name}, {model_version})")

# # Plotting
# fig, ax = plt.subplots()
# ax.scatter(costs, accuracies)

# # Get the limits of the axes to help determine label placement
# x_lim = ax.get_xlim()
# y_lim = ax.get_ylim()

# # Determine the width of the plot
# plot_width = x_lim[1] - x_lim[0]

# for i, label in enumerate(labels):
#     # Calculate the normalized position of the point within the plot
#     normalized_x_position = (costs[i] - x_lim[0]) / plot_width

#     # Choose alignment based on position to avoid overflow
#     if normalized_x_position > 0.8:  # Adjust threshold as needed
#         ha = 'right'
#     else:
#         ha = 'left'

#     # Place text with adjusted alignment
#     ax.text(costs[i], accuracies[i], label, ha=ha, va='bottom', fontsize=9)

# # Add a grid with dotted lines
# ax.grid(True, which='both', linestyle=':', color='gray', linewidth=0.5)

# ax.set_xlabel('Kosten in Dollar')
# ax.set_ylabel('Genauigkeit')

# # Save to file
# file_path = '/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/simple_cost_vs_accuracy.png'
# fig.savefig(file_path)

import json
import matplotlib.pyplot as plt

# Assuming the JSON data is loaded into 'data'
path_for_data = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/simple_results_gpt4.json"

with open(path_for_data, 'r') as file:
    data = json.load(file)

# Prepare data for plotting
costs = [metrics['costs'] for metrics in data.values()]
accuracies = [metrics['accuracy'] for metrics in data.values()]
labels = list(data.keys())

# Plotting
fig, ax = plt.subplots()
scatter = ax.scatter(costs, accuracies)

# Get limits and center
x_lim = ax.get_xlim()
y_lim = ax.get_ylim()
center_x = (x_lim[1] + x_lim[0]) / 2
center_y = (y_lim[1] + y_lim[0]) / 2

# Find the data point that is furthest to the right and left to adjust labels accordingly
right_most = max(costs)
left_most = min(costs)

for i, label in enumerate(labels):
    # Set the initial alignment to the center
    ha = 'center'
    va = 'center'
    
    # Adjust horizontal alignment based on data point position
    if costs[i] > center_x:
        ha = 'left' if costs[i] != right_most else 'right'
    elif costs[i] < center_x:
        ha = 'right' if costs[i] != left_most else 'left'

    # Add some offset to prevent the label from being on the dot
    x_offset = (x_lim[1] - x_lim[0]) * 0.01
    y_offset = (y_lim[1] - y_lim[0]) * 0.01

    # Adjust the position based on the alignment
    x_text = costs[i] + x_offset if ha == 'left' else costs[i] - x_offset
    y_text = accuracies[i] + y_offset if va == 'bottom' else accuracies[i] - y_offset

    # Add the label with a background box
    ax.text(x_text, y_text, label, ha=ha, va='bottom', fontsize=9, bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', boxstyle='round,pad=0.2'))

ax.set_xlim(x_lim)
ax.set_ylim(y_lim)
ax.grid(True, which='both', linestyle=':', color='gray', linewidth=0.5)
ax.set_xlabel('Kosten in Dollar')
ax.set_ylabel('Genauigkeit')

# Save to file
file_path = '/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/image.png'
fig.savefig(file_path, bbox_inches='tight')

# Show plot (for Jupyter Notebooks or similar environments)
plt.show()
