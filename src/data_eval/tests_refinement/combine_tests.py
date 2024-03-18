import json
path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/test_cases/0.2/io"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_tests_refinement"

mapping = {
    "gpt-3.5-turbo-0125": {
        "with_refinement": 3,
        "without_refinement": 3
    },
    "gpt-4-0125-preview": {
        "with_refinement": 2,
        "without_refinement": 3
    }
}

combined_results = []

for model, algorithms in mapping.items():
    for refinement, count in algorithms.items():
        for i in range(0, count):
            if refinement == "with_refinement":
                file_path = f"{path}/{model}/{refinement}/{model}/{i}/test_results_stats.json"
            else:
                file_path = f"{path}/{model}/{refinement}/{i}/test_results_stats.json"
            with open(file_path, "r") as f:
                data = json.load(f)
                combined_results.append({
                    "model": model,
                    "refinement": refinement,
                    "accuracy": data["accuracy"],
                })


with open(f"{save_path}/combined_results.jsonl", "w") as f:
    for result in combined_results:
        f.write(json.dumps(result) + "\n")