import numpy as np
import json
import os

# Fetch the environment variable 'DEV_PATH' defined in your system
DEV_PATH = os.getenv('DEV_PATH')

path = f"{DEV_PATH}/src/benchmark_results/test_cases/0.2/codeT/gpt-3.5-turbo-0125/without_refinement"
save_path = f"{DEV_PATH}/src/benchmark_results/test_cases/0.2/codeT/gpt-3.5-turbo-0125/without_refinement"

mapping = {
    "codeT": {
        "gpt-3.5-turbo-0125": {
            "without_refinement": {}
        }
    }
}

def get_pass_at_1_for_method():
    sum_of_accuracy = 0
    for i in range(3):
        current_path = f"{path}/{i}/test_results_stats.json"
        with open(current_path, "r") as f:
            data = json.load(f)
            sum_of_accuracy += data["accuracy"]
    return sum_of_accuracy / 3

sum_of_accuracy = get_pass_at_1_for_method()

# save
with open(f"{save_path}/pass_at_1.json", "w") as f:
    json.dump({ "pass_at_1": sum_of_accuracy}, f)

                

