import json
import os

base_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/reflection"

mapping = {
    "simple_simple": {
        "0.8_0.8": {
           "gpt-3.5-turbo-0125": {
              "use_best": ["predefined"]
           }
        },
        "0.6_0.6": {
            "gpt-4-0125-preview": {
                "use_best": ["predefined"]
            }
        },
    }
}

for method, temp_model_mapping in mapping.items():
    for temp, models in temp_model_mapping.items():
        for model, reflection_types in models.items():
            for reflection_type, test_types in reflection_types.items():
                for test_type in test_types:
                    if model == "gpt-3.5-turbo-0125":
                        max_items = 5
                    elif model == "gpt-4-0125-preview":
                        max_items = 3
                    results_path = f"{base_path}/{method}/{temp}/{model}/{reflection_type}/{test_type}/results_for_{max_items}"
                    for i in range(10):
                        k = i + 1
                        current_file_i = f"{results_path}/{k}/combined_results.jsonl"
                        current_file_i_content = []
