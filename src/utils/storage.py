import numpy as np
import json
import os
#TODO: Only one load_object function is enough.

humanEval_file_path = '/home/neuravity/dev/prompt_engineering/src/human_eval/data/HumanEval.jsonl'
humanEval_50_file_path = '/home/neuravity/dev/prompt_engineering/src/human_eval/data/HumanEval_50.jsonl'
static_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results"
test_cases_path = "/home/neuravity/dev/prompt_engineering/src/human_eval/data/ExtractedTests.json"

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

def save_generated_tests(items, prompt_type, model):
    # Assuming static_path is the base directory where all benchmarks are stored

    base_path = f"{static_path}/test_cases/{prompt_type}/{model}"
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

def save_benchmark_results_for_reflection(items, benchmark_type, strategy, file_name_config):
    # Base directory path as per specifications
    base_path = f"{static_path}/{benchmark_type}/{strategy}"
    os.makedirs(base_path, exist_ok=True)
    
    # Construct the file name from the file_name_config values, excluding use_gpt-4_at_round if it's None
    file_name_elements = [
        file_name_config['rounds'],
        file_name_config['prompt_for_reflection'],
        file_name_config['prompt_for_refinement'],
        file_name_config['model_for_reflection'],
        file_name_config['model_for_refinement']
    ]
    # Add use_gpt-4_at_round to the list if it's not None
    if file_name_config.get('use_gpt-4_at_round') is not None:
        file_name_elements.append(str(file_name_config['use_gpt-4_at_round']))
    
    # Join the elements to form the base file name
    file_name_base = "_".join(map(str, file_name_elements))
    
    # Initialize the file prefix and determine the unique directory and file path
    file_prefix = 0
    while True:
        potential_dir_name = f"{file_prefix}_{file_name_base}"
        potential_file_name = f"{potential_dir_name}.jsonl"
        # New: Create a directory with the same name as the base file name inside the base path
        full_dir_path = os.path.join(base_path, potential_dir_name)
        full_file_path = os.path.join(full_dir_path, potential_file_name)
        if not os.path.exists(full_file_path):
            os.makedirs(full_dir_path, exist_ok=True)  # Ensure the directory is created
            break
        file_prefix += 1
    
    # Write the items to the new file
    with open(full_file_path, 'w') as file:
        for item in items:
            file.write(json.dumps(item) + '\n')
    
    return full_file_path

def create_file_for_reflection(benchmark_type, strategy, file_name_config):
    # Assuming static_path is defined elsewhere in your code
    base_path = f"{static_path}/{benchmark_type}/{strategy}"
    os.makedirs(base_path, exist_ok=True)
    
    # Construct the name_config from the file_name_config values, excluding 'rounds'
    name_config_elements = [
        file_name_config['prompt_for_reflection'],
        file_name_config['prompt_for_refinement'],
        file_name_config['model_for_reflection'],
        file_name_config['model_for_refinement']
    ]
    if file_name_config.get('use_gpt-4_at_round') is not None:
        name_config_elements.append(str(file_name_config['use_gpt-4_at_round']))
    name_config = "_".join(map(str, name_config_elements))
    
    # Find the highest existing prefix for the given name_config
    highest_prefix = -1
    for entry in os.listdir(base_path):
        if os.path.isdir(os.path.join(base_path, entry)) and name_config in entry:
            try:
                prefix = int(entry.split('_')[0])
                highest_prefix = max(highest_prefix, prefix)
            except ValueError:
                continue
    
    # Determine the path of the latest file if it exists
    if highest_prefix != -1:
        latest_dir_name = f"{highest_prefix}_{name_config}"
        latest_file_name = f"{latest_dir_name}.jsonl"
        full_dir_path = os.path.join(base_path, latest_dir_name)
        full_file_path = os.path.join(full_dir_path, latest_file_name)
        
        # Check if the file has less than 164 items
        if os.path.exists(full_file_path):
            with open(full_file_path, 'r') as file:
                items = file.readlines()
                if len(items) < 164:
                    # Return the current file path if not finished
                    return full_file_path
    
    # If the process reaches here, it means a new file is needed
    new_prefix = highest_prefix + 1
    new_dir_name = f"{new_prefix}_{name_config}"
    new_file_name = f"{new_dir_name}.jsonl"
    full_new_dir_path = os.path.join(base_path, new_dir_name)
    full_new_file_path = os.path.join(full_new_dir_path, new_file_name)
    
    os.makedirs(full_new_dir_path, exist_ok=True)  # Ensure the directory is created
    open(full_new_file_path, 'w').close()  # Create an empty file
    
    return full_new_file_path

def save_result(item, path):
    """
    Saves an item to a .jsonl file at the specified path.

    Args:
    - item (dict): The item to be saved.
    - path (str): The file path where the item should be saved.
    """
    with open(path, 'a') as file:  # Open the file in append mode
        file.write(json.dumps(item) + '\n')  # Serialize the item to JSON and append a newline

def load_test_cases():
    test_cases = []
    with open(test_cases_path, 'r') as file:
        for line in file:
            try:
                test_case = json.loads(line)
                test_cases.append(test_case)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from line: {line}")
                print(f"Exception: {e}")
                # Handle the error or continue
    return test_cases

def load_from_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
def load_data_from_jsonl(file_path):
    data = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Parse each line as a JSON object and append to the data list
                data.append(json.loads(line))
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file at {file_path}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return data
