import json

path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/test_cases/0.2"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_tests_using_methods"

methods = ["io", "synth_few_shot", "zero_shot_cot"]
models = ["gpt-3.5-turbo-0125", "gpt-4-0125-preview"]

combined_results = []

for method in methods:
    for model in models:
        file_path = f"{path}/{method}/{model}/without_refinement/0/test_results_stats.json"
        with open(file_path, "r") as f:
            data = json.load(f)
            combined_results.append({
                "model": model,
                "method": method,
                "test_type": "without_refinement",
                "accuracy": data["accuracy"]
            })

with open(f"{save_path}/combined_results.json", "w") as f:
    json.dump(combined_results, f, indent=4)