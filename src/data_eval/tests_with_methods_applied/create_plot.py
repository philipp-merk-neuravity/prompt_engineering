import matplotlib.pyplot as plt
import json

path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_tests_with_methods_applied/combined_results.jsonl"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/images/test_methods_applied"

test_name_mapping = {
    "tests_4_4": "GPT-4 (Zero-Shot)",
    "tests_3.5_synth_few_shot": "GPT-3.5 (Synth. Few-Shots)",
    "tests_3.5_zero_shot_cot": "GPT-3.5 (Zero-Shot CoT)",
    "tests_4_4_synth_few_shot": "GPT-4 (Synth. Few-Shots)",
    "tests_4_4_zero_shot_cot": "GPT-4 (Zero-Shot CoT)",
    "tests_3.5": "GPT-3.5 (Zero-Shot)",
    "tests_3.5_synth_few_shot": "GPT-3.5 (Synth. Few-Shots)",
    "tests_3.5_zero_shot_cot": "GPT-3.5 (Zero-Shot CoT)"
}

prompt_model_mapping = {
    "gpt-4-0125-preview": "GPT-4",
    "gpt-3.5-turbo-0125": "GPT-3.5"
}

# Load the data
with open(path, "r") as f:
    data = [json.loads(line) for line in f]

# Organize data by model
model_data = {}
for d in data:
    prompt_model_label = prompt_model_mapping[d['prompt_model']]
    test_name_label = test_name_mapping[d['test_name']]
    label = f"{test_name_label}"  # Use test name for labels within each plot
    if prompt_model_label not in model_data:
        model_data[prompt_model_label] = {}
    if label not in model_data[prompt_model_label]:
        model_data[prompt_model_label][label] = []
    model_data[prompt_model_label][label].append((d['sample_size'], d['accuracy']))

# Plotting
for model_label, plot_data in model_data.items():
    plt.figure(figsize=(10, 8))
    for label, points in plot_data.items():
        points.sort()  # Sort points by sample size
        sample_sizes, accuracies = zip(*points)  # Unpack points into two lists
        plt.plot(sample_sizes, accuracies, label=label)

    plt.xlabel('Samples')
    plt.ylabel('Genauigkeit')
    plt.legend()
    plt.tight_layout()
    plt.grid()

    plt.savefig(f"{save_path}/{model_label}_accuracy_vs_sample_size.png")