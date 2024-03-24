import json
import os

# Fetch the environment variable 'DEV_PATH' defined in your system
DEV_PATH = os.getenv('DEV_PATH')


path = f"{DEV_PATH}/src/benchmark_results/code_gen/simple_check_tests"
save_path = f"{DEV_PATH}/src/benchmark_results/results/data/eval_tests_refinement_applied"


mapping = {
    "0.6": {
        "io": {
            "gpt-4-0125-preview": ["tests_3.5_zero_shot", "tests_3.5_3.5_zero_shot", "tests_4_zero_shot", "tests_4_4_zero_shot"]
        }
    },
    "0.8": {
        "io": {
            "gpt-3.5-turbo-0125": ["tests_3.5_zero_shot", "tests_3.5_3.5_zero_shot"]
        }
    }
}

combined_results = []

for temperature, methods in mapping.items():
    for method, models in methods.items():
        for model, test_types in models.items():
            for test_type in test_types:
                current_folder_path = f"{path}/{temperature}/{method}/{model}/{test_type}"
                for i in range(10):
                    current_file_path = f"{current_folder_path}/{i}/1_stats.json"
                    with open(current_file_path, "r") as f:
                        data = json.load(f)
                        combined_results.append({
                            "temperature": temperature,
                            "method": method,
                            "model": model,
                            "test_type": test_type,
                            "accuracy": data["accuracy"]["pass@1"],
                            "sample_size": i + 1
                        })

with open(f"{save_path}/combined_stats.jsonl", "w") as f:
    for result in combined_results:
        f.write(json.dumps(result) + "\n")