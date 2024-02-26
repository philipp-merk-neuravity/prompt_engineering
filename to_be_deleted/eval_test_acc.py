import json

# Paths to the datasets
path_for_tests = "/home/neuravity/dev/prompt_engineering/src/human_eval/data/ExtractedTests.json"
path_for_human_eval = "/home/neuravity/dev/prompt_engineering/src/human_eval/data/HumanEval.jsonl"

# Load the test cases
with open(path_for_tests, 'r') as file:
    test_cases = json.load(file)

# Load the HumanEval tasks
with open(path_for_human_eval, 'r') as file:
    human_eval_tasks = [json.loads(line) for line in file]

# Function to find tests for a given task_id
def find_tests_for_task(task_id, test_cases):
    for test_case in test_cases:
        if test_case['task_id'] == task_id:
            return test_case['tests']
    return []

# Execute tests for each task
for task in human_eval_tasks:
    task_id = task['task_id']
    code_solution = task['prompt'] + "\n" + task['canonical_solution']
    tests = find_tests_for_task(task_id, test_cases)
    if not tests:
        print(f"No tests found for {task_id}")
        continue
    
    # Define the function from the task prompt
    exec(code_solution)

    # Execute each test
    for test in tests:
        exec_code = f"def candidate(*args, **kwargs):\n\treturn {task['entry_point']}(*args, **kwargs)\n{test}"
        try:
            exec(exec_code)
        except NameError as e:
            print(f"NameError encountered for {task_id}: {e}")
        except AssertionError:
            print(f"Test failed for {task_id}")
        except Exception as e:
            print(f"Unexpected error for {task_id}: {e}")

