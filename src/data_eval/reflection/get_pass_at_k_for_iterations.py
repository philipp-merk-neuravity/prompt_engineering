import json
import os
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()
# Fetch the environment variable 'DEV_PATH' defined in your system
DEV_PATH = os.getenv('DEV_PATH')


base_path = f"{DEV_PATH}/src/benchmark_results/code_gen/reflection"
script_path = f"{DEV_PATH}/src/human_eval/human_eval/evaluate_functional_correctness.py"
problem_file_path=f"{DEV_PATH}/src/human_eval/data/HumanEval.jsonl"

mapping = {
    "simple_simple": {
        "0.8_0.8": {
           "gpt-3.5-turbo-0125": {
              "use_next": ["predefined"],
              "use_best": ["predefined"]
           }
        },
        "0.8_0.6": {
            "gpt-4-0125-preview": {
                "use_next": ["predefined"],
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
                    max_items = 10
                    results_path = f"{base_path}/{method}/{temp}/{model}/{reflection_type}/{test_type}/results_for_{max_items}"
                    for i in range(10):
                        k = i + 1
                        current_file_i = f"{results_path}/{k}/combined_results.jsonl"
                        command = [
                            "python", script_path,
                            "--sample_file", current_file_i,
                            "--problem_file", problem_file_path,
                            "--k", "1",
                            # Include other command line arguments as needed
                        ]
                        subprocess.run(command)

