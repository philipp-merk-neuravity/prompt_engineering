import json
import matplotlib.pyplot as plt

save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/img/test_cases"

# Load data from a JSON file
file_path = '/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_tests/test_results_with_efficiency.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Define a function to create a unique name for each method
def create_method_name(entry):
    refinement_part = "with refinement" if entry["refinement_model"] else "without refinement"
    return f"{entry['model']} ({entry['refinement_model']})"

# Extract method names and corresponding values
methods = [create_method_name(entry) for entry in data]
utility_scores = [entry["efficiency"] for entry in data]
accuracies = [entry["accuracy"] for entry in data]
total_costs = [entry["total_cost"] for entry in data]

# Function to plot the data
def plot_data(y_values, ylabel, filename, width=0.4):  # Add width parameter with default value
    plt.figure(figsize=(10, 5))
    plt.bar(methods, y_values, color=['#add8e6', '#f0a868', '#98fb98', '#d3d3d3'], width=width)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")  # Rotate method names for better visibility
    plt.tight_layout()  # Adjust layout to not cut off labels
    plt.savefig(save_path + '/' + filename)
    plt.close()

# Plot each of the metrics with thinner bars
plot_data(utility_scores, 'Genauigkeit/Kosten', 'utility_scores_by_method.png')
plot_data(accuracies, 'Genauigkeit', 'accuracies_by_method.png')
plot_data(total_costs, 'Kosten', 'total_costs_by_method.png')
