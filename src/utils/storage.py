import numpy as np
import json
import os
from dotenv import load_dotenv

load_dotenv()
# Fetch the environment variable 'DEV_PATH' defined in your system
DEV_PATH = os.getenv('DEV_PATH')

humanEval_file_path = f'{DEV_PATH}/src/human_eval/data/HumanEval.jsonl'
humanEval_50_file_path = f'{DEV_PATH}/src/human_eval/data/HumanEval_50.jsonl'
static_path = f"{DEV_PATH}/src/benchmark_results"
test_cases_path = f"{DEV_PATH}/src/human_eval/data/ExtractedTests.json"

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

def save_benchmark_results(items, benchmark_type, strategy, prompt_type, model, temperature):
    # Assuming static_path is the base directory where all benchmarks are stored
    base_path = f"{static_path}/{benchmark_type}/{strategy}/{temperature}/{prompt_type}/{model}"
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

def save_generated_tests(items, prompt_type, model, model_for_refinement, use_refinement, temperature):
    base_path = ""
    if use_refinement:
        base_path = f"{static_path}/test_cases/{temperature}/{prompt_type}/{model}/with_refinement/{model_for_refinement}"
    else:
        base_path = f"{static_path}/test_cases/{temperature}/{prompt_type}/{model}/without_refinement"
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

def create_file_for_iterative_sampling(test_case_type):
    base_path = f"{static_path}/code_gen/iterative_sampling/{test_case_type}"
    os.makedirs(base_path, exist_ok=True)

    # get the highest prefix
    highest_prefix = -1
    for entry in os.listdir(base_path):
        if os.path.isdir(os.path.join(base_path, entry)):
            try:
                prefix = int(entry.split('_')[0])
                highest_prefix = max(highest_prefix, prefix)
            except ValueError:
                continue

    # check if the file has less than 164 items
    if highest_prefix != -1:
        latest_dir_name = f"{highest_prefix}_{test_case_type}"
        latest_file_name = f"{latest_dir_name}.jsonl"
        full_dir_path = os.path.join(base_path, latest_dir_name)
        full_file_path = os.path.join(full_dir_path, latest_file_name)

        if os.path.exists(full_file_path):
            with open(full_file_path, 'r') as file:
                items = file.readlines()
                if len(items) < 164:
                    return full_file_path

    # if the process reaches here, it means a new file is needed
    new_prefix = highest_prefix + 1
    new_dir_name = f"{new_prefix}_{test_case_type}"
    new_file_name = f"{new_dir_name}.jsonl"
    full_new_dir_path = os.path.join(base_path, new_dir_name)
    full_new_file_path = os.path.join(full_new_dir_path, new_file_name)

    os.makedirs(full_new_dir_path, exist_ok=True)

    open(full_new_file_path, 'w').close()

    return full_new_file_path
    
# def create_file_for_reflection(strategy, folder_path_config, file_name_config):
#     # Assuming static_path is defined elsewhere in your code
#     base_path = f"{static_path}/{strategy}"
#     os.makedirs(base_path, exist_ok=True)
    
#     # Construct the name_config from the file_name_config values, excluding 'rounds'
#     name_config = "_".join([str(file_name_config[key]) for key in file_name_config])
    
#     # Find the highest existing prefix for the given name_config
#     highest_prefix = -1
#     for entry in os.listdir(base_path):
#         if os.path.isdir(os.path.join(base_path, entry)) and name_config in entry:
#             try:
#                 prefix = int(entry.split('_')[0])
#                 highest_prefix = max(highest_prefix, prefix)
#             except ValueError:
#                 continue
    
#     # Determine the path of the latest file if it exists
#     if highest_prefix != -1:
#         latest_dir_name = f"{highest_prefix}_{name_config}"
#         latest_file_name = f"{latest_dir_name}.jsonl"
#         full_dir_path = os.path.join(base_path, latest_dir_name)
#         full_file_path = os.path.join(full_dir_path, latest_file_name)
        
#         # Check if the file has less than 164 items
#         if os.path.exists(full_file_path):
#             with open(full_file_path, 'r') as file:
#                 items = file.readlines()
#                 if len(items) < 164:
#                     # Return the current file path if not finished
#                     return full_file_path
    
#     # If the process reaches here, it means a new file is needed
#     new_prefix = highest_prefix + 1
#     new_dir_name = f"{new_prefix}_{name_config}"
#     new_file_name = f"{new_dir_name}.jsonl"
#     full_new_dir_path = os.path.join(base_path, new_dir_name)
#     full_new_file_path = os.path.join(full_new_dir_path, new_file_name)
    
#     os.makedirs(full_new_dir_path, exist_ok=True)  # Ensure the directory is created
#     open(full_new_file_path, 'w').close()  # Create an empty file
    
#     return full_new_file_path

def create_file_for_reflection(static_path, folder_path_config):
    import os
    
    # Building the correct base path from the folder_path_config, handling mixed types
    base_path = static_path
    for folder_names in folder_path_config:
        # Convert all elements to string and then join them
        folder_name = "_".join([str(element) for element in folder_names])
        base_path = os.path.join(base_path, folder_name)
        os.makedirs(base_path, exist_ok=True)  # Ensure the directory exists

    # Determine the highest numerical folder
    subfolders = [f for f in os.listdir(base_path) if f.isdigit()]
    highest_num = max(map(int, subfolders)) if subfolders else -1

    # Path for the highest existing or new numerical folder
    num_folder_path = os.path.join(base_path, str(highest_num))
    
    # Constructing the file name from file_name_config, correctly joining elements
    file_name = f"{highest_num}.jsonl"
    full_file_path = os.path.join(num_folder_path, file_name)

    # Checking if the file exists in the highest numerical folder and its line count
    if os.path.exists(full_file_path):
        with open(full_file_path, 'r') as file:
            items = file.readlines()
            if len(items) < 164:
                # If the file exists and has less than 164 lines, return its path
                return full_file_path

    # If reaching this point, either no suitable file was found or we need a new folder
    new_num = highest_num + 1
    new_num_folder_path = os.path.join(base_path, str(new_num))
    os.makedirs(new_num_folder_path, exist_ok=True)  # Create the new numerical folder
    # New file path in the new numerical folder
    file_name = f"{new_num}.jsonl"
    new_full_file_path = os.path.join(new_num_folder_path, file_name)
    open(new_full_file_path, 'w').close()  # Create an empty new file
    
    return new_full_file_path


def save_result(item, path):
    """
    Saves an item to a .jsonl file at the specified path.

    Args:
    - item (dict): The item to be saved.
    - path (str): The file path where the item should be saved.
    """
    with open(path, 'a') as file:  # Open the file in append mode
        file.write(json.dumps(item) + '\n')  # Serialize the item to JSON and append a newline

def load_test_cases(test_cases_path: str):
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
    
def load_from_jsonl(file_path):
    items = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            item = json.loads(line.strip())
            items.append(item)
    return items

def load_multiline_data_from_jsonl(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            # Wrap the file content in square brackets and replace the last comma with an empty space if needed
            json_content = "[" + file_content.rstrip(',') + "]"
            data = json.loads(json_content)
            return data
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file at {file_path}: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []
