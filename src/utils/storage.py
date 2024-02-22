import numpy as np
import json
import os

humanEval_file_path = '/home/neuravity/dev/prompt_engineering/src/human_eval/data/HumanEval.jsonl'
humanEval_50_file_path = '/home/neuravity/dev/prompt_engineering/src/human_eval/data/HumanEval_50.jsonl'
static_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results"
test_cases_path = "/home/neuravity/dev/prompt_engineering/test.jsonl"

def load_benchmark(type: str = 'all'):
    json_objects = []
    benchmark_data_path = None
    if type == 'all':
        benchmark_data_path = humanEval_file_path
    elif type == '50':
        benchmark_data_path = humanEval_50_file_path
    try:
        # Open the .jsonl file directly without gzip
        with open(benchmark_data_path, 'r', encoding='utf-8') as file:
            for line in file:
                json_obj = json.loads(line)
                json_objects.append(json_obj)
    except Exception as e:
        # Handle exceptions such as file not found or JSON decode error
        print(f"An error occurred: {e}")
        return []

    return json_objects

def load_benchmark_results(benchmark_results_file_path: str):
    json_objects = []

    with open(benchmark_results_file_path, 'r') as file:
        for line in file:
            json_obj = json.loads(line)
            json_objects.append(json_obj)
            
    return np.array(json_objects, dtype=object)

# def save_benchmark_results(item: dict, benchmark_type: str, strategy: str, prompt_type: str, model: str, file_id: str):
#     current_file_path = "{benchmark_type}/{strategy}/{prompt_type}/{model}/{file_id}/{file_id}.jsonl"
#     with open(benchmark_results_file_path, 'a') as file:
#         file.write(json.dumps(item) + '\n')

def save_benchmark_results(items, benchmark_type, strategy, prompt_type, model):
    # Assuming static_path is the base directory where all benchmarks are stored

    base_path = f"{static_path}/{benchmark_type}/{strategy}/{prompt_type}/{model}"
    os.makedirs(base_path, exist_ok=True)
    
    # Determine the next available file_id by inspecting existing folders
    existing_ids = [int(name) for name in os.listdir(base_path) if name.isdigit()]
    file_id = max(existing_ids) + 1 if existing_ids else 0
    
    # Create the specific directory for this file_id
    specific_path = f"{base_path}/{file_id}"
    os.makedirs(specific_path, exist_ok=True)  # This correctly creates the directory
    
    # Define the file path where the results will be stored
    benchmark_results_file_path = f"{specific_path}/{file_id}.jsonl"
    
    # Write the items to the file
    with open(benchmark_results_file_path, 'a') as file:
        for item in items:
            file.write(json.dumps(item) + '\n')
    
    return benchmark_results_file_path  # Optionally return the file path for further use


def load_test_cases():
    with open(test_cases_path, 'r') as file:
        return file.read()