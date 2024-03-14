import json
base_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/test_cases/few_shot"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_tests"
costs_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/costs.json"

with open(costs_path, 'r') as file:
    costs = json.load(file)

models = [
    "gpt-3.5-turbo-0125",
    "gpt-4-0125-preview"
]

types = [
    "with_refinement",
    "without_refinement"
]

refinement_models = {
    "gpt-3.5-turbo-0125": ["gpt-3.5-turbo-0125", "gpt-4-0125-preview"],
    "gpt-4-0125-preview": ["gpt-4-0125-preview"]
}

combined_results = []

for model in models:
    for type in types:
        if type == "with_refinement":
            for refinement_model in refinement_models[model]:
                path = f"{base_path}/{model}/{type}/{refinement_model}/test_results_stats.json"
                # read the file
                with open(path, 'r') as file:
                    data = json.load(file)
                combined_results.append({
                    "model": model,
                    "type": type,
                    "refinement_model": refinement_model,
                    "data": data
                })
        else:
            path = f"{base_path}/{model}/{type}/test_results_stats.json"
            # read the file
            with open(path, 'r') as file:
                data = json.load(file)
            combined_results.append({
                "model": model,
                "type": type,
                "refinement_model": None,
                "data": data
            })

with open(f"{save_path}/test_results.jsonl", 'w') as file:
    for result in combined_results:
        file.write(json.dumps(result) + '\n')