import json
import os

# Fetch the environment variable 'DEV_PATH' defined in your system
DEV_PATH = os.getenv('DEV_PATH')


base_path = f"{DEV_PATH}/src/benchmark_results/code_gen/simpe_check_tests"
save_path = f"{DEV_PATH}/src/benchmark_results/results/data/eval_tests_with_samples"

mapping = {
    "0.6": {
        "io": {
            "gpt-4-0125-preview": [
                "tests_3.5",
                "tests_3.5_3.5",
                "tests_4",
                "tests_4_4"
            ]
        }, 
    },
    "0.8": {
        "io": {
            "gpt-3.5-turbo-0125": [
                "tests_3.5",
                "tests_3.5_3.5",
            ]
        }, 
    },
}

combined_results = []

for temperature, methods in mapping.items():
    for method, models in methods.items():
        for model, test_types in models.items():
            for test_type in test_types:
                folder_path = f"{base_path}/{temperature}/{method}/{model}/{test_type}"
                for i in range(10):
                    file_path = f"{folder_path}/{i}/1_stats.json"
                    with open(file_path, "r") as f:
                        current_result = json.load(f)
                        combined_results.append({
                            "temperature": temperature,
                            "method": method,
                            "model": model,
                            "sample_size": i + 1,
                            "test_type": test_type,
                            "accuracy": current_result["accuracy"]["pass@1"]
                        })
                        
with open(f"{save_path}/combined_samples.jsonl", "w") as f:
    for result in combined_results:
        f.write(json.dumps(result) + "\n")