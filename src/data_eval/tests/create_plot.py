import matplotlib.pyplot as plt
import json

# Define the path to your JSONL file
path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_tests/test_results_with_costs.json"

# Mapping for labels
mapping_for_labels = {
    "gpt-3.5-turbo-0125": "3.5",
    "gpt-4-0125-preview": "4",
}

# Read data from the file
data = []
with open(path, "r") as file:
    data = json.load(file)

# Prepare data for plotting
x_labels = []
accuracies = []
for entry in data:
    model_label = mapping_for_labels[entry["model"]]
    refinement_model_label = mapping_for_labels.get(entry["refinement_model"], "")
    combined_label = f"({model_label}/{refinement_model_label})" if refinement_model_label else f"({model_label})"
    x_labels.append(combined_label)
    accuracies.append(entry["accuracy"])

# Plotting
fig, ax = plt.subplots()
ax.bar(x_labels, accuracies, color='skyblue')
ax.set_xlabel('Model/Refinement Model')
ax.set_ylabel('Accuracy')
ax.set_title('Model Accuracy Comparison')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("/home/neuravity/dev/prompt_engineering/src/test_results.png")
