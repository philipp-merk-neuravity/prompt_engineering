import matplotlib.pyplot as plt
import json
import os
from dotenv import load_dotenv

load_dotenv()
# Fetch the environment variable 'DEV_PATH' defined in your system
DEV_PATH = os.getenv('DEV_PATH')


path = f"{DEV_PATH}/src/benchmark_results/results/data/eval_refl_keep_best/combined_results.jsonl"
save_path = f"{DEV_PATH}/src/benchmark_results/images/keep_best"

label_mapping = {
    "use_best": "Beste Lösung",
    "use_next": "Nächste Lösung",
}

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
        label = label_mapping[reflection_type]
        plt.plot(iterations, accuracies, label=label)
    
    plt.xlabel("Iteration", fontsize=10)
    plt.ylabel("Genauigkeit", fontsize=10)
    plt.legend(fontsize=8)
    plt.grid(True)
    plt.savefig(f"{save_path}/{model}.png", dpi=700)