from typing import List
import re

def convert_tests_to_list(tests: str) -> List[str]:
    return tests.split('\n')

def parse_code_solution(code_solution: str) -> str:
    pattern = r"```python\n(.*?)```"
    match = re.search(pattern, code_solution, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return code_solution
    
def extract_function_body(code_solution: str) -> str:
    # Find the end of the docstring
    end_of_docstring = code_solution.find('"""', code_solution.find('"""') + 3) + 3
    # Extract everything after the docstring as the function body
    return "    " + code_solution[end_of_docstring:].strip()
    
def convert_unit_test_results_to_str(unit_test_results: object) -> str:
    # shape: {'passed_tests': ['assert has_close_elements([1.0, 2.0, 3.0], 0.5) == False', 'assert has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3) == True', 'assert has_close_elements([1.0, 2.0, 3.0, 4.0, 5.0], 0.5) == False'], 'failed_tests': ['assert has_close_elements([1.0, 2.0, 3.0], 0.1) == True', 'assert has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.6) == False', 'assert has_close_elements([1.0, 2.0, 3.0, 4.0, 5.0], 1.0) == True']}
    return f"Tests passing:\n{unit_test_results['passed_tests']}\nTests failing:\n{unit_test_results['failed_tests']}"