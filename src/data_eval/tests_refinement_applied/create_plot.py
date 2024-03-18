import json
import matplotlib.pyplot as plt

# Path to your data
path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_tests_with_prompt_methods/combined_results.json"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/images/tests_prompt_methods"

# Label mapping
label_mapping = {
    "io": "Zero-Shot",
    "synth_few_shot": "Synth. Few-Shots",
    "zero_shot_cot": "Zero-Shot CoT",
}

# Load the data
with open(path, "r") as f:
    data = json.load(f)

# Use the mapping to update labels
categories = [f"{label_mapping[d['prompt_method']]} + {d['model']}" for d in data]
accuracies = [d["data"]["accuracy"] for d in data]

# Plotting
plt.figure(figsize=(10, 8))
plt.bar(categories, accuracies, color='skyblue')
plt.ylabel('Genauigkeit')
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Save the plot
plt.savefig(f"{save_path}/combined_results.png")
