import os
import json
import matplotlib.pyplot as plt

# Define methods and their paths
methods = [
    {"name": "Reflexion (3, vordefiniert)", "path": "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/reflection/gpt3.5_predefined/results_per_iteration/"},
    {"name": "Reflection (3, 3, 3)", "path": "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/reflection/gpt3.5_gpt3.5_gpt3.5/results_per_iteration"},
    {"name": "Reflection (3, 3, 4)", "path": "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/reflection/gpt3.5_gpt3.5_gpt4/results_per_iteration"},
    {"name": "Sampling (3, vordefiniert)", "path": "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/iterative_sampling/gpt3.5_predefined/results_per_iteration/"},
    {"name": "Sampling (3, 3, 3)", "path": "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/iterative_sampling/gpt3.5_gpt3.5_gpt3.5/results_per_iteration"},
    {"name": "Sampling (3, 3, 4)", "path": "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/iterative_sampling/gpt3.5_gpt3.5_gpt4/results_per_iteration"},
    {"name": "Reflexion (4, 3, 4)", "path": "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/reflection/gpt4_gpt3.5_gpt4/results_per_iteration"},
    {"name": "Reflexion (4, vordefiniert)", "path": "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/reflection/gpt4_predefined/results_per_iteration"},
    {"name": "Sampling (4, 3, 4)", "path": "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/iterative_sampling/gpt4_gpt3.5_gpt4/results_per_iteration"},
    {"name": "Sampling (4, vordefiniert)", "path": "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/iterative_sampling/gpt4_predefined/results_per_iteration"},
]

# Initialize dictionary to hold accuracies for each method
accuracies = {method['name']: [] for method in methods}
iterations = list(range(10))

# Process files for each method
for method in methods:
    for i in iterations:
        file_path = os.path.join(method['path'], str(i), f"iteration_{i}.jsonl_stats.json")
        with open(file_path, 'r') as file:
            data = json.load(file)
            accuracies[method['name']].append(data["accuracy"]["pass@1"])

plt.figure(figsize=(10, 6))

colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k']  # Extend this list if you have more methods
linestyles = ['-', '--', '-.', ':']

for idx, (method_name, method_accuracies) in enumerate(accuracies.items()):
    color = colors[idx % len(colors)]
    linestyle = linestyles[idx % len(linestyles)]
    # Plot without markers
    plt.plot(iterations, method_accuracies, linestyle=linestyle, color=color, label=method_name)

plt.xlabel("Iteration")
plt.ylabel("Genauigkeit (pass@1)")
plt.ylim(0.7, 1)  # Setting the y-axis to range from 0 to 1

# Place legend outside and below the plot
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), shadow=True, ncol=3)

plt.grid(True)
plt.tight_layout()  # Adjust layout to not cut off labels

# Save the plot
plt.savefig("accuracy_comparison_over_iterations.png")
