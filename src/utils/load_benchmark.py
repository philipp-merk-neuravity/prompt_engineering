import numpy as np
import json
import gzip

file_path = '/home/neuravity/dev/prompt_engineering/src/human_eval/data/HumanEval.jsonl.gz'

def load_benchmark():
    json_objects = []

    # Open the .gz file using gzip.open instead of the regular open
    with gzip.open(file_path, 'rt', encoding='utf-8') as file:
        for line in file:
            json_obj = json.loads(line)
            json_objects.append(json_obj)
            
    return np.array(json_objects, dtype=object)
