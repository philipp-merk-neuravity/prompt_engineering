import json
import matplotlib.pyplot as plt

path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_prompt_method_gen_tests/combined_samples.jsonl"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/images/sampling_gen_tests"
with open(path, "r") as f:
    results = [json.loads(line) for line in f]

organized_data = {}
for entry in results:
    model = entry["model"]
    method = entry["method"]
    sample_size = entry["sample_size"]
    accuracy = entry["accuracy"]
    
    if model not in organized_data:
        organized_data[model] = {}
    if method not in organized_data[model]:
        organized_data[model][method] = []
    organized_data[model][method].append((sample_size, accuracy))

# Sort data for plotting
for model, methods in organized_data.items():
    for method in methods:
        organized_data[model][method].sort()

# Plotting
for model, methods in organized_data.items():
    plt.figure(figsize=(10, 6))
    for method, data in methods.items():
        sample_sizes = [x[0] for x in data]
        accuracies = [x[1] for x in data]
        plt.plot(sample_sizes, accuracies, label=method)
    
    plt.title(f"Model: {model}")
    plt.xlabel("Sample Size")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True)
    # save
    plt.savefig(f"{save_path}/{model}.png")