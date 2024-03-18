import matplotlib.pyplot as plt
import json

path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_tests_with_methods_applied/combined_results.jsonl"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/images/test_methods_applied"

test_name_mapping = {
    "tests_4": "GPT-4 (Zero-Shot)",
    "gpt_3.5_synth_few_shot": "GPT-3.5 (Synth. Few-Shots)",
    "gpt_3.5_zero_shot_cot": "GPT-3.5 (Zero-Shot CoT)",
    "gpt_4_synth_few_shot": "GPT-4 (Synth. Few-Shots)",
    "gpt_4_zero_shot_cot": "GPT-4 (Zero-Shot CoT)",
    "tests_3.5": "GPT-3.5 (Zero-Shot)",
    "gpt_3.5_synth_few_shot": "GPT-3.5 (Synth. Few-Shots)",
    "gpt_3.5_zero_shot_cot": "GPT-3.5 (Zero-Shot CoT)"
}

prompt_model_mapping = {
    "gpt-4-0125-preview": "GPT-4",
    "gpt-3.5-turbo-0125": "GPT-3.5"
}

with open(path, "r") as f:
    data = [json.loads(line) for line in f]

plot_data = {}
for d in data:
    test_name_label = test_name_mapping[d['test_name']]
    prompt_model_label = prompt_model_mapping[d['prompt_model']]
    label = f"{prompt_model_label} + {test_name_label}"
    if label not in plot_data:
        plot_data[label] = []
    plot_data[label].append((d['sample_size'], d['accuracy']))

# Plotting
plt.figure(figsize=(10, 8))
for label, points in plot_data.items():
    points.sort()  # Sort points by sample size
    sample_sizes, accuracies = zip(*points)  # Unpack points into two lists
    plt.plot(sample_sizes, accuracies, label=label)

plt.xlabel('Samples')
plt.ylabel('Genauigkeit')
plt.legend()
plt.tight_layout()

plt.savefig(f"{save_path}/accuracy_vs_sample_size.png")
