import json

path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/simpe_check_tests"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_tests_with_methods_applied"

mapping = {
    "0.6": {
        "io": {
            "gpt-4-0125-preview": ["tests_4_4", "tests_3.5_synth_few_shot", "tests_3.5_zero_shot_cot", "tests_4_4_synth_few_shot", "tests_4_4_zero_shot_cot"]
        },
    },
    "0.8": {
        "io": {
            "gpt-3.5-turbo-0125": ["tests_3.5", "tests_3.5_synth_few_shot", "tests_3.5_zero_shot_cot"]
        },
    }
}

combined_results = []

for temperature, prompt_methods in mapping.items():
    for prompt_method, prompt_models in prompt_methods.items():
        for prompt_model, test_names in prompt_models.items():
            for test_name in test_names:
                current_path = f"{path}/{temperature}/{prompt_method}/{prompt_model}/{test_name}"
                for i in range(10):
                    current_file_path = f"{current_path}/{i}/1_stats.json"
                    with open(current_file_path, "r") as f:
                        data = json.load(f)
                        combined_results.append({
                            "temperature": temperature,
                            "prompt_method": prompt_method,
                            "prompt_model": prompt_model,
                            "test_name": test_name,
                            "accuracy": data["accuracy"]["pass@1"],
                            "sample_size": i + 1
                        })


with open(f"{save_path}/combined_results.jsonl", "w") as f:
    for result in combined_results:
        f.write(json.dumps(result) + "\n")