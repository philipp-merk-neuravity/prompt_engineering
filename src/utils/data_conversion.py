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