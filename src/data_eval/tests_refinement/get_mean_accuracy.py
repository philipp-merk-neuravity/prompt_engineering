import json
path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_tests_refinement/combined_results.jsonl"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_tests_refinement"

refinement_types = ["with_refinement", "without_refinement"]
model_types = ["gpt-3.5-turbo-0125", "gpt-4-0125-preview"]

with open(path, "r") as f:
    data = [json.loads(line) for line in f]

combined_results = []

for model in model_types:
    for refinement in refinement_types:
        accuracies = [result["accuracy"] for result in data if (result["model"] == model and result["refinement"] == refinement)]
        mean_accuracy = sum(accuracies) / len(accuracies)
        combined_results.append({
            "model": model,
            "refinement": refinement,
            "accuracy": mean_accuracy
        })

# Save the combined results to a file
with open(f"{save_path}/combined_results_mean.jsonl", "w") as f:
    for result in combined_results:
        f.write(json.dumps(result) + "\n")