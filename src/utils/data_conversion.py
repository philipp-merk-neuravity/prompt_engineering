from typing import List, Optional
import re
import ast
import json

def convert_tests_to_list(tests: str, prompt_type: str) -> List[str]:
    # first extract ```pythoncode``` block
    tests = parse_code_block(tests)

    if prompt_type == "agentCoder":
        tests_dict = json.loads(tests)
        assert_statements = []
        # Iterate through each category of tests ('basic', 'edge')
        for category in tests_dict:
            # Iterate through each test scenario in the category
            for test_scenario in tests_dict[category]:
                # Extract the 'test' string from each scenario
                assert_statements.append(test_scenario['test'])
        return assert_statements
    parts = tests.split('assert')[1:]
    # Prepend 'assert ' (with a space) back to each part and strip leading/trailing whitespace/newlines
    assert_statements = ['assert ' + part.strip() for part in parts]
    # Remove the comment from each assert statement using "#" as the delimiter
    assert_statements = [assert_statement.split('#')[0].strip() for assert_statement in assert_statements]
    return assert_statements
    
def parse_code_block(string: str) -> Optional[str]:

    code_pattern = r"```python(.*?)```"
    match = re.search(code_pattern, string, re.DOTALL)

    if match:
        return match.group(1).strip()

    return string

def extract_python_code_from_json(json_string, prompt_type):
    data = json.loads(json_string)

    if prompt_type == "synth_few_shot":
        python_code = data["Original Problem Solution"]["Python3 Code"]
    if prompt_type == "agentCoder":
        python_code = data["code_solution"]
    if prompt_type == "reflection_and_refinement":
        python_code = data["refined implementation"]
    return python_code

def convert_unit_test_results_to_str(unit_test_results: object) -> str:
    unit_test_results_as_str = f"Passed Tests:\n{unit_test_results['passed_tests']}\nFailed Tests:\n{unit_test_results['failed_tests']}"
    return unit_test_results_as_str

import ast

def check_is_syntax_correct(code):
    try:
        namespace = {}
        exec("from typing import *\n" + code, namespace)
        ast.parse(code)
        return True, None  # No error message since the code is deemed correct
    except SyntaxError as e:
        # Creating a detailed error message for syntax errors
        error_message = f"Syntax error: {e.msg} at line {e.lineno}, offset {e.offset}"
        return False, error_message
    except Exception as e:
        # Catching other exceptions and returning a generic error message
        return False, f"Error: {str(e)}"


def filter_syntactically_correct_tests_ast(tests):
    correct_tests = []
    incorrect_tests = []

    for test in tests:
        try:
            ast.parse(test)
            correct_tests.append(test)
        except SyntaxError:
            incorrect_tests.append(test)

    return correct_tests

def split_tests_into_individual_functions(unit_tests: List[str]) -> list:
    return ["def check(candidate):\n    " + test for test in unit_tests]

def extract_function_name(code):
    """
    Extracts the name of the first function defined in the given code.
    """
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            return node.name  # Return the name of the first function found
    return None  # Return None if no function definition is found

def remove_function_definition_from_test(test: str) -> str:
    test_without_def = test[test.index("\n") + 1:]
    return "\n".join(line[4:] if line.startswith("    ") else line for line in test_without_def.split("\n"))

def get_unresolved_tasks(benchmark_data, results):
    unresolved_tasks = []
    for benchmark_item in benchmark_data:
        item_is_resolved = False
        for result in results:
            if benchmark_item["task_id"] == result["task_id"]:
                item_is_resolved = True
                break
        if item_is_resolved == False:
            unresolved_tasks.append(benchmark_item)
    return unresolved_tasks