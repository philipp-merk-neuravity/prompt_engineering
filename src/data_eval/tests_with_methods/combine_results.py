import json
import os
from dotenv import load_dotenv

load_dotenv()
# Fetch the environment variable 'DEV_PATH' defined in your system
DEV_PATH = os.getenv('DEV_PATH')


path = f"{DEV_PATH}/src/benchmark_results/test_cases/0.2"
save_path = f"{DEV_PATH}/src/benchmark_results/results/data/eval_tests_with_methods"

mapping = {
    "io": {
        "gpt-3.5-turbo-0125": {
            "without_refinement": 3
        },
        "gpt-4-0125-preview": {
            "with_refinement": 2
        },
    },
    "synth_few_shot": {
        "gpt-3.5-turbo-0125": {
            "without_refinement": 3
        },
        "gpt-4-0125-preview": {
            "with_refinement": 3
        }
    },
    "zero_shot_cot": {
        "gpt-3.5-turbo-0125": {
            "without_refinement": 3
        },
        "gpt-4-0125-preview": {
            "with_refinement": 3
        }
    }
}

combined_results = []
combined_mean_results = []

for prompt_method, models in mapping.items():
    for model, refinements in models.items():
        for refinement, item_count in refinements.items():
            current_sum_of_accuracy = 0
            if refinement == "without_refinement":
                current_folder_path = f"{path}/{prompt_method}/{model}/{refinement}"
            else: 
                current_folder_path = f"{path}/{prompt_method}/{model}/{refinement}/{model}"
            for i in range(item_count):
                current_file_path = f"{current_folder_path}/{i}/test_results_stats.json"
                with open(current_file_path, "r") as f:
                    data = json.load(f)
                    current_sum_of_accuracy += data["accuracy"]
                    combined_results.append({
                        "prompt_method": prompt_method,
                        "model": model,
                        "refinement": refinement,
                        "accuracy": data["accuracy"],
                    })
            mean_accuracy = current_sum_of_accuracy / item_count
            combined_mean_results.append({
                "prompt_method": prompt_method,
                "model": model,
                "refinement": refinement,
                "accuracy": mean_accuracy,
            })

with open(f"{save_path}/combined_results.jsonl", "w") as f:
    for item in combined_results:
        f.write(json.dumps(item) + "\n")

with open(f"{save_path}/combined_mean_results.jsonl", "w") as f:
    for item in combined_mean_results:
        f.write(json.dumps(item) + "\n")

