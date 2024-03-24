import json
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()
# Fetch the environment variable 'DEV_PATH' defined in your system
DEV_PATH = os.getenv('DEV_PATH')


path = f"{DEV_PATH}/src/benchmark_results/results/data/eval_prompt_method/combined_results_prompt_method.jsonl"
save_path = f"{DEV_PATH}/src/benchmark_results/images/prompt_method"

results = []

label_mapping = {
    "io": "Zero-Shot",
    "scot": "SCoT",
    "synth_few_shot_split": "Synth. Few-Shots",
    "zero_shot_cot": "Zero-Shot CoT",
}

with open(path, "r") as f:
    for line in f:
        results.append(json.loads(line))

data_by_model = {}
for entry in results:
    model = entry['model']
    method = entry['method']
    if model not in data_by_model:
        data_by_model[model] = {}
    if method not in data_by_model[model]:
        data_by_model[model][method] = {'k': [], 'accuracy': []}
    data_by_model[model][method]['k'].append(entry['k'])
    data_by_model[model][method]['accuracy'].append(entry['accuracy'])

# Plotting
for model, methods_data in data_by_model.items():
    plt.figure(figsize=(10, 6))
    for method, data in methods_data.items():
        label = label_mapping[method]
        plt.plot(data['k'], data['accuracy'], label=label)
    plt.xlabel('Pass@k', fontsize=13)
    plt.ylabel('Genauigkeit', fontsize=13)
    plt.legend()
    plt.grid(True)
    # Save each plot as a separate file, named after the model
    plt.savefig(f'{save_path}/{model}.png', dpi=700)
    plt.close()  # Close the figure to free memory