import json
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()
# Fetch the environment variable 'DEV_PATH' defined in your system
DEV_PATH = os.getenv('DEV_PATH')


path = f"{DEV_PATH}/src/benchmark_results/results/data/eval_tests_with_samples/combined_samples.jsonl"
save_path = f"{DEV_PATH}/src/benchmark_results/images/sampling_check_test"

with open(path, "r") as f:
    results = [json.loads(line) for line in f]

data_grouped = {} 

for entry in results:
    key = (entry['model'], entry['test_type'])
    if key not in data_grouped:
        data_grouped[key] = []
    data_grouped[key].append((entry['sample_size'], entry['accuracy']))

plt.figure(figsize=(10, 6))
for key, value in data_grouped.items():
    sorted_values = sorted(value, key=lambda x: x[0])
    sample_sizes = [x[0] for x in sorted_values]
    accuracies = [x[1] for x in sorted_values]
    plt.plot(sample_sizes, accuracies, label=f'{key[0]}, {key[1]}')

plt.xlabel('Samples')
plt.ylabel('Genauigkeit')
plt.legend()
plt.grid()
plt.savefig(f"{save_path}/sampling_check_test.png")
