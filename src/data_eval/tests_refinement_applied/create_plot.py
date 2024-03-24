import json
import matplotlib.pyplot as plt
from collections import defaultdict
import os
from dotenv import load_dotenv

load_dotenv()
# Fetch the environment variable 'DEV_PATH' defined in your system
DEV_PATH = os.getenv('DEV_PATH')


# Path to your data
path = f"{DEV_PATH}/src/benchmark_results/results/data/eval_tests_refinement_applied/combined_stats.jsonl"
save_path = f"{DEV_PATH}/src/benchmark_results/images/test_refinement_applied"

label_mapping = {
    "gpt-3.5-turbo-0125": "3.5",
    "gpt-4-0125-preview": "4"
}

# Open and read the data file
with open(path, "r") as f:
    data = [json.loads(line) for line in f]

# Organize data by model and test_type combination
data_by_combination = defaultdict(list)
for entry in data:
    key = (entry["model"], entry["test_type"])
    data_by_combination[key].append((entry["sample_size"], entry["accuracy"]))

# Plotting
plt.figure(figsize=(10, 6))  # Adjust the figure size as needed

for key, values in data_by_combination.items():
    # Sort values by sample_size to ensure a coherent line plot
    sorted_values = sorted(values, key=lambda x: x[0])
    sample_sizes = [sv[0] for sv in sorted_values]
    accuracies = [sv[1] for sv in sorted_values]
    label = "("
    if key[0] == "gpt-4-0125-preview":
        label += "4, "
    elif key[0] == "gpt-3.5-turbo-0125":
        label += "3.5, "
    if key[1] == "tests_3.5_zero_shot":
        label += "3.5, -)"
    elif key[1] == "tests_3.5_3.5_zero_shot":
        label += "3.5, 3.5)"
    elif key[1] == "tests_4_zero_shot":
        label += "4, -)"
    elif key[1] == "tests_4_4_zero_shot":
        label += "4, 4)"
    # Plot each combination as a separate line
    plt.plot(sample_sizes, accuracies, label=label)

plt.xlabel('Samples', fontsize=13)
plt.ylabel('Genauigkeit', fontsize=13)
plt.legend()
plt.grid()
plt.tight_layout()

plt.savefig(f"{save_path}/accuracy_by_sample_size.png", dpi=700)