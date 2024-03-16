import json
import os
import subprocess

base_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/reflection"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/images/keep_best_gen_tests"

mapping = {
    "simple_simple": {
        "0.8_0.8": {
           "gpt-3.5-turbo-0125": {
                "use_next": ["gpt_3.5-turbo-0125_gpt-4-0125-preview"],
                "use_next_x_use_best": ["gpt_3.5-turbo-0125_gpt-4-0125-preview"]
           }
        },
        "0.8_0.6": {
            "gpt-4-0125-preview": {
                "use_next_x_use_best": ["gpt_3.5-turbo-0125_gpt-4-0125-preview"],
                "use_next": ["gpt_3.5-turbo-0125_gpt-4-0125-preview"]
            }
        },
    }
}

combined_results = []

for method, temp_model_mapping in mapping.items():
    for temp, models in temp_model_mapping.items():
        for model, reflection_types in models.items():
            for reflection_type, test_types in reflection_types.items():
                for test_type in test_types:
                    max_iterations = 10
                    current_path = f"{base_path}/{method}/{temp}/{model}/{reflection_type}/{test_type}"
                    for i in range(max_iterations):
                        i = i + 1
                        current_file_i = f"{current_path}/results_for_10/{i}/1_stats.json"
                        with open(current_file_i, "r") as f:
                            current_file_i_content = json.load(f)
                        current_file_i_content["iteration"] = i
                        current_file_i_content["reflection_type"] = reflection_type
                        current_file_i_content["test_type"] = test_type
                        current_file_i_content["model"] = model
                        current_file_i_content["temp"] = temp
                        combined_results.append(current_file_i_content)


with open(f"{save_path}/combined_results.jsonl", "w") as f:
    # line by line 
    for result in combined_results:
        f.write(json.dumps(result) + "\n")