from eval_tests import run_main
import os
import json
import argparse
from dotenv import load_dotenv

load_dotenv()
DEV_PATH = os.getenv('DEV_PATH')

base_path = f"{DEV_PATH}/src/benchmark_results/test_cases/0.2"

def run_test_eval(mapping, save_path):
    for method, models in mapping.items():
        for model, refinement_types in models.items():
            for refinement_type, refinement_models in refinement_types.items():
                for refinement_model in refinement_models:
                    if refinement_type == "with_refinement":
                        current_path = f"{base_path}/{method}/{model}/{refinement_type}/{refinement_model}"
                    else:
                        current_path = f"{base_path}/{method}/{model}/{refinement_type}"
                    for i in range(3):
                        current_path_i = f"{current_path}/{i}/{i}.jsonl"
                        run_main(current_path_i)

    combined_stats = []

    for method, models in mapping.items():
        for model, refinement_types in models.items():
            for refinement_type, refinement_models in refinement_types.items():
                for refinement_model in refinement_models:
                    if refinement_type == "with_refinement":
                        current_path = f"{base_path}/{method}/{model}/{refinement_type}/{refinement_model}"
                    else:
                        current_path = f"{base_path}/{method}/{model}/{refinement_type}"
                    current_mean_accuracy = 0
                    current_accuracy_sum = 0
                    for i in range(3):
                        current_path_i = f"{current_path}/{i}/test_results_stats.json"
                        with open(current_path_i, "r") as f:
                            data = json.load(f)
                            current_accuracy_sum += data["accuracy"]
                    current_mean_accuracy = current_accuracy_sum / 3

                    combined_stats.append({
                        "model": model,
                        "method": method,
                        "refinement_type": refinement_type,
                        "refinement_model": refinement_model,
                        "accuracy": current_mean_accuracy,
                    })


    with open(f"{save_path}/combined_stats.jsonl", "w") as f:
        for result in combined_stats:
            f.write(json.dumps(result) + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run async tasks for code generation with iterative refinement.')
    parser.add_argument('--mapping_path', type=str, required=True, help='Path to the mapping file.')
    parser.add_argument('--save_path', type=str, required=True, help='Path to save the combined stats.')
    args = parser.parse_args()

    with open(args.mapping_path, "r") as f:
        mapping = json.load(f)
    
    run_test_eval(mapping, args.save_path)