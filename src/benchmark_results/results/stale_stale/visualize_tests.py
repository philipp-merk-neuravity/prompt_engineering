import json
from matplotlib import pyplot as plt
import numpy as np

path_for_tests = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_tests/test_results_with_normalized_costs_and_utility.json"


# Load the test results

with open(path_for_tests, 'r') as file:
    data = json.load(file)

# Prepare data
labels = [f'{d["model"]}{" + " + d["refinement_model"] if d["refinement_model"] else ""}' for d in data]
accuracy = [d["accuracy"] for d in data]
total_cost = [d["total_cost"] for d in data]
utility_score = [d["utility_score"] for d in data]
x = np.arange(len(labels))  # the label locations

# Plot settings
fig, axs = plt.subplots(3, 1, figsize=(12, 18))

# Accuracy
axs[0].bar(x, accuracy, color='skyblue')
axs[0].set_title('Accuracy (Precision)')
axs[0].set_xticks(x)
axs[0].set_xticklabels(labels, rotation=45, ha="right")
axs[0].set_ylabel('Accuracy')

# Total Cost
axs[1].bar(x, total_cost, color='lightgreen')
axs[1].set_title('Total Cost')
axs[1].set_xticks(x)
axs[1].set_xticklabels(labels, rotation=45, ha="right")
axs[1].set_ylabel('Total Cost')

# Utility Score
axs[2].bar(x, utility_score, color='salmon')
axs[2].set_title('Utility Score')
axs[2].set_xticks(x)
axs[2].set_xticklabels(labels, rotation=45, ha="right")
axs[2].set_ylabel('Utility Score')

plt.tight_layout()

# Save the plot
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/img/test_cases"
plt.savefig(save_path + "/test_results_with_normalized_costs_and_utility.png")