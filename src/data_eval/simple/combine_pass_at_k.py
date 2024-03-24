import subprocess
import json
import os
import argparse
from dotenv import load_dotenv

load_dotenv()
# Fetch the environment variable 'DEV_PATH' defined in your system
DEV_PATH = os.getenv('DEV_PATH')


# Define the path to the script you want to run
base_path = f"{DEV_PATH}/src/benchmark_results/code_gen/simple"

def run_combine_pass_at_k(mapping, save_path):
    results = []
    for temp, method_model_mapping in mapping.items():
        for method, models in method_model_mapping.items():
            for model in models:
                current_path = f"{base_path}/{temp}/{method}/{model}"
                for i in range(10):
                    k = i + 1
                    current_path_i = f"{current_path}/{i}/{k}_stats.json"
                    
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

    with open(save_path, "w") as f:
        for result in results:
            f.write(json.dumps(result) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run async tasks for code generation with iterative refinement.')
    parser.add_argument('--mapping_path', type=str, help='Mapping folder structure.')
    parser.add_argument('--save_path', type=str, help='Path to save the combined results.')
    args = parser.parse_args()

    with open(args.mapping_path, 'r') as f:
        mapping = json.load(f)

    run_combine_pass_at_k(mapping, args.save_path)
