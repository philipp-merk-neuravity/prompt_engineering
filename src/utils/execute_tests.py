from typing import *
import ast

def extract_function_name(code):
    """
    Extracts the name of the first function defined in the given code.
    """
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            return node.name  # Return the name of the first function found
    return None  # Return None if no function definition is found

def split_tests_into_individual_functions(unit_tests: List[str]) -> list:
    return ["def check(candidate):\n    " + test for test in unit_tests]

def remove_function_definition_from_test(test: str) -> str:
    test_without_def = test[test.index("\n") + 1:]
    return "\n".join(line[4:] if line.startswith("    ") else line for line in test_without_def.split("\n"))

def add_imports_to_code_solution(code_solution: str) -> str:
    return "from typing import *\n" + code_solution

def run_tests(solution_code: str, tests: list):
    namespace = {}
    exec(solution_code, namespace)

    function_name = extract_function_name(solution_code)
    if not function_name:
        raise ValueError("No function definition found in the provided code solution.")
    solution_function = namespace[function_name]

    results = {
        "passed_tests": [],
        "failed_tests": []
    }

    for test in tests:
        test_namespace = dict(namespace)

        try:
            exec(test, test_namespace)
            test_namespace['check'](solution_function)
            results["passed_tests"].append(remove_function_definition_from_test(test))
        except AssertionError:
            results["failed_tests"].append(remove_function_definition_from_test(test))

    return results

def check_is_solved(tests: List[str]) -> bool:
    return len(tests) == 0

def get_test_results(code_solution: str, tests: str):
    individual_tests = split_tests_into_individual_functions(tests)
    code_solution = add_imports_to_code_solution(code_solution)
    test_results = run_tests(code_solution, individual_tests)  
    is_solved = check_is_solved(test_results["failed_tests"])
    return test_results, is_solved
