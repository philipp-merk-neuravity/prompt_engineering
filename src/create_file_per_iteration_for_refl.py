from utils.storage import load_from_jsonl
import json
import os  # Import the os module

# Load the data
path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/reflection/gpt3.5_predefined/combined_results.jsonl"
data = load_from_jsonl(path)

# Initialize a dictionary to hold stats for each iteration
stats_for_iterations = {i: [] for i in range(0, 10)}

# Process data to fill stats_for_iterations
for item in data:
    iteration_states = item["iteration_states"]
    for i in range(0, 10):
        current_best_iteration = {}
        for state in iteration_states:
            if state["iteration"] <= i:
                current_best_iteration = state
        current_best_iteration["task_id"] = item["task_id"]
        stats_for_iterations[i].append(current_best_iteration)

# Save each iteration's stats to a separate file, line by line, in its own folder
base_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/reflection/gpt3.5_predefined/results_per_iteration"
for i in range(0, 10):
    iteration_path = os.path.join(base_path, str(i))  # Define the path for this iteration's folder
    os.makedirs(iteration_path, exist_ok=True)  # Create the folder (and any required parent folders)
    with open(os.path.join(iteration_path, f"iteration_{i}.jsonl"), "w") as f:
        for item in stats_for_iterations[i]:
            f.write(json.dumps(item) + "\n")