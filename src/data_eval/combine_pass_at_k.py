import subprocess
import json

# Define the path to the script you want to run
script_path = "/home/neuravity/dev/prompt_engineering/src/human_eval/human_eval/evaluate_functional_correctness.py"
problem_file_path="/home/neuravity/dev/prompt_engineering/src/human_eval/data/HumanEval.jsonl"
base_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/simple"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_prompt_method/results_prompt_method.jsonl"
mapping = {
    # "0.2": {
    #     "io": ["gpt-3.5-turbo-0125", "gpt-4-0125-preview"],
    # },
    # "0.4": {
    #     "io": ["gpt-3.5-turbo-0125", "gpt-4-0125-preview"],
    # },
    "0.6": {
        "io": ["gpt-4-0125-preview"],
        "scot": ["gpt-4-0125-preview"],
        "synth_few_shot_split": ["gpt-4-0125-preview"],
        "zero_shot_cot": ["gpt-4-0125-preview"],
    },
    "0.8": {
        "io": ["gpt-3.5-turbo-0125"],
        "scot": ["gpt-3.5-turbo-0125"],
        "synth_few_shot_split": ["gpt-3.5-turbo-0125"],
        "zero_shot_cot": ["gpt-3.5-turbo-0125"],
    }
}

results = []

for temp, method_model_mapping in mapping.items():
    for method, models in method_model_mapping.items():
        for model in models:
            current_path = f"{base_path}/{temp}/{method}/{model}"
            for i in range(10):
                k = i + 1
                current_path_i = f"{current_path}/{i}/{k}_stats.json"
                # read the stats file
                with open(current_path_i, "r") as f:
                    stats = json.load(f)
                results.append({
                    "temp": temp,
                    "method": method,
                    "model": model,
                    "k": k,
                    "accuracy": stats["accuracy"][f"pass@{k}"],
                    "prompt_tokens": stats["prompt_tokens"],
                    "completion_tokens": stats["completion_tokens"],
                    "duration": stats["duration"]
                })

# write the results to a file
with open(save_path, "w") as f:
    for result in results:
        f.write(json.dumps(result) + "\n")