import subprocess
import os
import argparse
import json
from dotenv import load_dotenv

load_dotenv()
DEV_PATH = os.getenv('DEV_PATH')

script_path = f"{DEV_PATH}/src/human_eval/human_eval/evaluate_functional_correctness.py"
problem_file_path=f"{DEV_PATH}/src/human_eval/data/HumanEval.jsonl"
base_path = f"{DEV_PATH}/src/benchmark_results/code_gen/simple"

def run_pass_at_k_eval(mapping):
    for temp, method_model_mapping in mapping.items():
        for method, models in method_model_mapping.items():
            for model in models:
                combined_results = []
                samples_path = f"{base_path}/{temp}/{method}/{model}"
                samples_combined_results_path = f"{samples_path}/combined_results.jsonl"
                for i in range(10):
                    k = i + 1
                    current_data_path = f"{samples_path}/{i}/{i}.jsonl"
                    with open(current_data_path) as f:
                        data = f.readlines()
                        combined_results.extend(data)
                
                with open(samples_combined_results_path, "w") as f:
                    f.writelines(combined_results)
                    
                for i in range(10):
                    k = i + 1
                    command = [
                        "python", script_path,
                        "--sample_file", samples_combined_results_path,
                        "--problem_file", problem_file_path,
                        "--k", str(k),
                    ]
                    subprocess.run(command)
                    save_path = f"{samples_path}/{i}"
                    stats_path = f"{samples_path}/{k}_stats.json"
                    results_path = f"{samples_path}/{k}_results.jsonl"

                    subprocess.run(["mv", stats_path, save_path])
                    subprocess.run(["mv", results_path, save_path])

            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run async tasks for code generation with iterative refinement.')
    parser.add_argument('--mapping_path', type=str, help='Mapping folder structure.')
    args = parser.parse_args()

    with open(args.mapping_path, 'r') as f:
        mapping = json.load(f)
        
    run_pass_at_k_eval(mapping)

