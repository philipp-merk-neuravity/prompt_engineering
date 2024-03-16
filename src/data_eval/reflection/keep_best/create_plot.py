import matplotlib.pyplot as plt
import json

path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_gen_tests/reflection/combined_results.jsonl"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/images/keep_best_gen_tests"

with open(path, "r") as f:
    data = [json.loads(line) for line in f]

# Filtering data by model
models = set(item["model"] for item in data)
reflection_types = set(item["reflection_type"] for item in data)

# Plotting
for model in models:
    plt.figure()
    for reflection_type in reflection_types:
        filtered_data = [item for item in data if item["model"] == model and item["reflection_type"] == reflection_type]
        iterations = [item["iteration"] for item in filtered_data]
        accuracies = [item["accuracy"]["pass@1"] for item in filtered_data]
        plt.plot(iterations, accuracies, label=reflection_type)
    
    plt.title(f"Model: {model}")
    plt.xlabel("Iteration")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{save_path}/{model}.png")