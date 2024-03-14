import json
import matplotlib.pyplot as plt

save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/img/simple_0.8/gpt3.5"

# Load data from a JSON file
file_path = '/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_prompt_method/0.8/gpt_3.5/results_simple_0.8_gpt_3.5_with_efficiency.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Assuming the structure inside the file is the same as the provided data
categories = data

# Define a list of colors for the lines
colors = {
    "Zero-Shot": "orange",
    "SCoT": "red",
    "Synth. Few-Shots": "blue",
    "Zero-Shot CoT": "green"
    # Add more colors if you have more categories
}

# Plotting Utility Score by Sample Size
plt.figure(figsize=(10, 6))

for category, data_points in categories.items():
    sample_sizes = [d["sample_size"] for d in data_points]
    utility_scores = [d["efficiency"] for d in data_points]
    plt.plot(sample_sizes, utility_scores, label=category, color=colors.get(category, 'black'))

plt.xlabel('Stichprobengröße')
plt.ylabel('Effizienz')
plt.legend()
plt.grid(True)

# Save the plot for Utility Score
plt.savefig(save_path + '/efficiency_by_sample_size_0.8.png')

# Clear the current plot for the next plot
plt.clf()

# Plotting Real Accuracy by Sample Size
plt.figure(figsize=(10, 6))

for category, data_points in categories.items():
    sample_sizes = [d["sample_size"] for d in data_points]
    accuracies = [d["accuracy"] for d in data_points]
    plt.plot(sample_sizes, accuracies, label=category, color=colors.get(category, 'black'))

plt.xlabel('Stichprobengröße')
plt.ylabel('Genauigkeit')
plt.legend()
plt.grid(True)

# Save the plot for Real Accuracy
plt.savefig(save_path + '/real_accuracy_by_sample_size_0.8.png')

# Clear the current plot for the next plot
plt.clf()

# Plotting Costs by Sample Size
plt.figure(figsize=(10, 6))

for category, data_points in categories.items():
    sample_sizes = [d["sample_size"] for d in data_points]
    costs = [d["total_cost"] for d in data_points]
    plt.plot(sample_sizes, costs, label=category, color=colors.get(category, 'black'))

plt.xlabel('Stichprobengröße')
plt.ylabel('Kosten in Dollar')
plt.legend()
plt.grid(True)

# Save the plot for Costs
plt.savefig(save_path + '/costs_by_sample_size_0.8.png')