import numpy as np
import json
import gzip
from utils.data_conversion import extract_function_body

benchmark_results_file_path = '/home/neuravity/dev/prompt_engineering/src/benchmark_results/benchmark_results.jsonl'
humanEval_file_path = '/home/neuravity/dev/prompt_engineering/src/human_eval/data/HumanEval.jsonl'

def load_benchmark():
    json_objects = []
    try:
        # Open the .jsonl file directly without gzip
        with open(humanEval_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                json_obj = json.loads(line)
                json_objects.append(json_obj)
    except Exception as e:
        # Handle exceptions such as file not found or JSON decode error
        print(f"An error occurred: {e}")
        return []

    return json_objects

def load_benchmark_results():
    json_objects = []

    with open(benchmark_results_file_path, 'r') as file:
        for line in file:
            json_obj = json.loads(line)
            json_objects.append(json_obj)
            
    return np.array(json_objects, dtype=object)

def save_benchmark_results(task_id: str, generated_code: str):
    completion = extract_function_body(generated_code)
    with open(benchmark_results_file_path, 'a') as file:
        file.write(json.dumps({"task_id": task_id, "completion": completion}) + "\n")
