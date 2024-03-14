import json
import matplotlib.pyplot as plt

path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_prompt_method/results_prompt_method.jsonl"

results = []

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
        plt.plot(data['k'], data['accuracy'], marker='o', label=method)
    plt.title(f'Model: {model}')
    plt.xlabel('k (pass@k)')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)
    # Save each plot as a separate file, named after the model
    plt.savefig(f'/home/neuravity/dev/prompt_engineering/src/{model}.png')
    plt.close()  # Close the figure to free memory