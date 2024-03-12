import matplotlib.pyplot as plt
import json

def load_from_jsonl(file_path):
    items = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            item = json.loads(line.strip())
            items.append(item)
    return items

base_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/simple"
temperatures = [0.2, 0.4, 0.6, 0.8]

# Dictionary to hold accuracy values for each temperature
accuracy_data = {temp: [] for temp in temperatures}

for temperature in temperatures:
    temperature_path = f"{base_path}/{temperature}/io/gpt-3.5-turbo-0125/results_for_10_samples"
    
    for i in range(1, 11):
        results_path = f"{temperature_path}/pass_at_{i}/combined_results.jsonl_stats.json"
        results = load_from_jsonl(results_path)
        # Assuming each result has only one entry and extracting the accuracy
        accuracy_data[temperature].append(results[0]['accuracy'])

sample_sizes = range(1, 11) # Assuming "pass@k" means k from 1 to 10
acc_02 = [list(v.values())[0] for v in accuracy_data[0.2]]
acc_04 = [list(v.values())[0] for v in accuracy_data[0.4]]
acc_06 = [list(v.values())[0] for v in accuracy_data[0.6]]
acc_08 = [list(v.values())[0] for v in accuracy_data[0.8]]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(sample_sizes, acc_02, label='Threshold=0.2')
plt.plot(sample_sizes, acc_04, label='Threshold=0.4')
plt.plot(sample_sizes, acc_06, label='Threshold=0.6')
plt.plot(sample_sizes, acc_08, label='Threshold=0.8')

plt.xlabel('Sample Size (pass@k)')
plt.ylabel('Genauigkeit')
plt.xticks(sample_sizes) # Ensuring x-axis ticks match the sample sizes
plt.yticks([i/10.0 for i in range(0, 11)]) # Setting y-axis to show 0 to 1
plt.ylim(0.6, 1)
plt.legend()
plt.grid(True)
# save the plot
plt.savefig(f"{base_path}/accuracy_by_sample_size.png")