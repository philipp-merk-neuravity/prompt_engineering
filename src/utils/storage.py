import numpy as np
import json
import gzip
from utils.data_conversion import extract_function_body

humanEval_file_path = '/home/neuravity/dev/prompt_engineering/src/human_eval/data/HumanEval.jsonl.gz'
benchmark_results_file_path = '/home/neuravity/dev/prompt_engineering/src/benchmark_results/benchmark_results.jsonl'

def load_benchmark():
    json_objects = []

    # Open the .gz file using gzip.open instead of the regular open
    with gzip.open(humanEval_file_path, 'rt', encoding='utf-8') as file:
        for line in file:
            json_obj = json.loads(line)
            json_objects.append(json_obj)
            
    return np.array(json_objects, dtype=object)

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
