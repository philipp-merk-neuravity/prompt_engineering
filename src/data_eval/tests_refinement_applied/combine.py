import json

path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/test_cases/0.2"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_tests_with_prompt_methods"
prompt_methods = ["io", "synth_few_shot", "zero_shot_cot"]

models = ["gpt-3.5-turbo-0125", "gpt-4-0125-preview"]

combined_results = []

for prompt_method in prompt_methods:
    for model in models:
        with open(f"{path}/{prompt_method}/{model}/without_refinement/0/test_results_stats.json", "r") as f:
            data = json.load(f)
            combined_results.append({
                "prompt_method": prompt_method,
                "model": model,
                "data": data
            })

with open(f"{save_path}/combined_results.json", "w") as f:
    json.dump(combined_results, f, indent=4)