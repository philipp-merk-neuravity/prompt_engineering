import json
import matplotlib.pyplot as plt
import os

# Fetch the environment variable 'DEV_PATH' defined in your system
DEV_PATH = os.getenv('DEV_PATH')


path = f"{DEV_PATH}/src/benchmark_results/results/data/temperature/combined_results_temp.jsonl"
save_path = f"{DEV_PATH}/src/benchmark_results/images/temperature"
results = []

with open(path, "r") as f:
    for line in f:
        results.append(json.loads(line))

# Assuming your results are already loaded into the `results` list

# Separate data by model
data_by_model = {}
for result in results:
    model = result["model"]
    if model not in data_by_model:
        data_by_model[model] = []
    data_by_model[model].append(result)

# Function to plot data for a single model
def plot_data_for_model(model_data, model_name):
    # Separate data by temperature
    data_by_temp = {}
    for entry in model_data:
        temp = entry["temp"]
        if temp not in data_by_temp:
            data_by_temp[temp] = {"k": [], "accuracy": []}
        data_by_temp[temp]["k"].append(entry["k"])
        data_by_temp[temp]["accuracy"].append(entry["accuracy"])
    
    plt.figure(figsize=(10, 6))
    for temp, values in data_by_temp.items():
        plt.plot(values["k"], values["accuracy"], label=f'Temp: {temp}')
    
    plt.xlabel('pass@k', fontsize=12)
    plt.ylabel('Genauigkeit', fontsize=12)
    plt.legend()
    plt.grid(True)
    # save
    plt.savefig(f"{save_path}/{model_name}.png", dpi=600)

# Plot data for each model
for model_name, model_data in data_by_model.items():
    plot_data_for_model(model_data, model_name)
