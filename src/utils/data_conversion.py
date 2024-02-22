from typing import List
import re
import ast
from typing import Optional
import json

def convert_tests_to_list(tests: str) -> List[str]:
    return tests.split('\n')

def parse_code_solution(code_solution: str) -> str:
    pattern = r"```python\n(.*?)```"
    match = re.search(pattern, code_solution, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return code_solution
    
def parse_code_block(string: str) -> Optional[str]:

    code_pattern = r"```python(.*?)```"
    match = re.search(code_pattern, string, re.DOTALL)

    if match:
        return match.group(1).strip()

    return string

def parse_first_func(code: str) -> str:
    # Split the code into lines
    code_lines = code.split("\n")
    
    # Initialize variables to track the start and end of the function
    def_i = -1
    end_i = None

    # Iterate over the lines to find the function definition and its end
    for i, line in enumerate(code_lines):
        if line.startswith("def ") and def_i == -1:
            def_i = i  # Mark the start of the function
        elif line.strip() == "" and def_i != -1 and end_i is None:
            # A blank line might indicate the end of the function, but it's not reliable
            continue
        elif def_i != -1 and (line.startswith("def ") or i == len(code_lines) - 1):
            # If another function definition starts or we reach the end of the code block
            end_i = i if line.startswith("def ") else i + 1
            break

    # Return None if no function definition is found
    if def_i == -1:
        return None

    # Correctly join and return the function's code
    return "\n".join(code_lines[def_i:end_i])

def add_imports_from_func_sig_to_code_solution (function_signature: str, code_solution: str) -> str:
    # Extract the imports from the function signature
    imports = re.findall(r"from .* import .*", function_signature)
    # Add the imports to the code solution
    return "\n".join(imports) + "\n" + code_solution

def add_typing_package_to_code_solution(code_solution: str) -> str:
    return "from typing import *\n" + code_solution

def remove_typing_package_from_code_solution(code_solution: str) -> str:
    return code_solution.replace("from typing import *\n", "")

def extract_function_body(code_solution: str) -> str:
    """
    Correctly extracts the body of a function from a given Python function definition
    by removing the first line that starts with 'def' and returning the rest of the function body as is.
    """
    # Split the code into lines
    lines = code_solution.split('\n')
    
    # Find the index of the line that starts with 'def'
    for i, line in enumerate(lines):
        if line.strip().startswith('def'):
            # Remove the 'def' line
            body_lines = lines[i+1:]
            break
    else:
        # If no 'def' line is found, return the original code
        return code_solution

    # Join the remaining lines back into a single string
    function_body = '\n'.join(body_lines)
    return function_body

def extract_python_code_from_json(json_string, prompt_type):
    data = json.loads(json_string)

    if prompt_type == "synth_few_shot":
        python_code = data["Original Problem Solution"]["Python3 Code"]
    if prompt_type == "agentCoder":
        python_code = data["code_solution"]
    return python_code

def convert_unit_test_results_to_str(unit_test_results: object) -> str:
    unit_test_results_as_str = f"Tested passed:\n{unit_test_results['passed_tests']}\nTests failed:\n{unit_test_results['failed_tests']}"
    return unit_test_results_as_str

def check_is_syntax_correct(code):
    try:
        ast.parse(code)
        return True, None  # No error message since the code is correct
    except SyntaxError as e:
        # Creating a detailed error message
        error_message = f"Syntax error: {e.msg} at line {e.lineno}, offset {e.offset}"
        return False, error_message

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
