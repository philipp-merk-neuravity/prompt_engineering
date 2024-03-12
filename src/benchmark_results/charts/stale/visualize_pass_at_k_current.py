import json
import matplotlib.pyplot as plt


path_for_data = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_prompt_method/0.8/gpt_4/results_simple_0.8_gpt_4.jsonl"
data = {}

with open(path_for_data, 'r') as file:
    data = json.load(file)

plt.figure(figsize=(10, 8))

for category, results in data.items():
    sample_sizes = [int(list(result["accuracy"].keys())[0].split('@')[1]) for result in results]
    accuracies = [list(result["accuracy"].values())[0] for result in results]
    plt.plot(sample_sizes, accuracies, '-o', label=category)

plt.xlabel('Sample Size (pass@k)')
plt.ylabel('Accuracy')
plt.title('Accuracy vs. Sample Size')
plt.legend()
plt.grid(True)


# save
plt.savefig("accuracy_vs_sample_size.png")