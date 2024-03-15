import json
import re

path_for_tests = "/home/neuravity/dev/prompt_engineering/src/human_eval/data/ExtractedTests.json"
path_for_solutions = "/home/neuravity/dev/prompt_engineering/src/human_eval/data/HumanEval.jsonl"

with open(path_for_tests, "r") as f:
    tests = json.load(f)

with open(path_for_solutions, "r") as f:
    solutions = [json.loads(line) for line in f]


def execute_test(solution: str, test_code: str, func_name: str):
    # Replace 'candidate' with the actual function name used in the solution
    test_code_modified = test_code.replace("candidate", func_name)
    namespace = {}
    try:
        # Execute solution and modified test code in the namespace
        exec(solution, namespace)
        exec(test_code_modified, namespace)
    except AssertionError:
        # Test failed
        return False
    except Exception as e:
        # Other execution errors (e.g., syntax error, name error)
        print(f"An error occurred: {e}")
        return False
    # Test passed
    return True

def find_function_name(solution: str):
    # Attempt to find the function definition in the solution
    import re
    match = re.search(r"def (\w+)\(", solution)
    if match:
        return match.group(1)
    else:
        return None

def execute_tests_for_solution(solution: str, tests: list):
    func_name = find_function_name(solution)
    if not func_name:
        print("No function definition found in the solution.")
        return 
    
    for test_code in tests:
        if not execute_test(solution, test_code, func_name):
            # If any test fails, return False immediately
            return False
    # All tests passed
    return True

# Assuming you have loaded 'tests' and 'solutions' from the files as before

failed_tests = []
correct_tests = []

for item in solutions:
    for item_test in tests:
        if item["task_id"] == item_test["task_id"]:
            solution_code = item["prompt"] + "\n" + item["canonical_solution"]
            tests_to_run = item_test["tests"]
            is_correct = execute_tests_for_solution(solution_code, tests_to_run)
            if not is_correct:
                failed_tests.append(item["task_id"])
            else:
                correct_tests.append(item["task_id"])
# Print the results
print(failed_tests)