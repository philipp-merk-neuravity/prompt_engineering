import matplotlib.pyplot as plt
import numpy as np
import json

# Function to read JSON data from a file
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Define the file path to the JSON data
static_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/"
file_path_for_performance = static_path + "test_cases_results.json"

# Read data from the JSON file
data_performance = read_json_file(file_path_for_performance)

# Process the data for plotting
methods = list(set(data_performance["gpt-3.5-turbo"].keys()) | set(data_performance["gpt-4-turbo"].keys()))  # Get unique method names
gpt3_accuracies = [data_performance["gpt-3.5-turbo"].get(method, {}).get("accuracy", 0) for method in methods]
gpt4_accuracies = [data_performance["gpt-4-turbo"].get(method, {}).get("accuracy", 0) for method in methods]

x = np.arange(len(methods))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, gpt3_accuracies, width, label='GPT-3', color='skyblue')
rects2 = ax.bar(x + width/2, gpt4_accuracies, width, label='GPT-4', color='orange')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Genauigkeit')
ax.set_xticks(x)
ax.set_xticklabels(methods, rotation=45, ha="right")
ax.legend(ncol=2)
ax.set_ylim([0, max(gpt3_accuracies + gpt4_accuracies) * 1.25])  # Assuming you want to increase space by 20%

# Function to auto-label the bars with their height values
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(round(height, 2)),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

fig.tight_layout()
plt.show()

# save the plot to a file

file_path = static_path + "test_cases_accuracy.png"
fig.savefig(file_path)
