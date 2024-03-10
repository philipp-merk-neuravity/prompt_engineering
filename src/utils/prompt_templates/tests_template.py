# TEST_GEN_INSTRUCTION_IO = "Write unique, diverse, and intuitive unit tests for functions given the signature and docstring. Answer with code only not in English. Use only assert statements that are independent from each other, e.g.: 'assert add3Numbers(1, 2, 3) == 6'"
TEST_GEN_INSTRUCTION_IO = "Write unique, diverse, and intuitive unit tests for functions given the signature and docstring. Answer with code only not in English. Use only assert statements that are independent from each other, e.g.: 'assert add3Numbers(1, 2, 3) == 6'"

TEST_GEN_CHAT_INSTRUCTION = """You are an AI coding assistant that can write unique, diverse, and intuitive unit tests for functions given the signature and docstring. Answer with code only not in English. Use only assert statements that are independent from each other, as shown in the example without additional code."""

TEST_GEN_CHAT_INSTRUCTION_SAVE="Create correct unit tests for the given function signature and docstring. Be careful to use inputs for you assert statements that you are likely to generate the correct output for. Answer with code only not in English. Use only assert statements that are independent from each other, e.g.: 'assert add3Numbers(1, 2, 3) == 6'."

TEST_GEN_ZERO_SHOT_INSTRUCTION = "Write unique, diverse, and intuitive unit tests for functions given the signature and docstring. Answer with code only containing comments. Use only assert statements that are independent from each other, e.g.: 'assert add3Numbers(1, 2, 3) == 6'. Think step by step by providing comments before each assert statement."

TEST_GEN_FEW_SHOT = """
Example:
[func signature]:
def add3Numbers(x, y, z):
    \"\"\" Add three numbers together.
    This function takes three numbers as input and returns the sum of the three numbers.
    \"\"\"
[unit tests]:
assert add3Numbers(1, 2, 3) == 6
assert add3Numbers(-1, 2, 3) == 4
assert add3Numbers(1, -2, 3) == 2
assert add3Numbers(1, 2, -3) == 0
assert add3Numbers(-3, -2, -1) == -6
assert add3Numbers(0, 0, 0) == 0
Task:
"""

TEST_GEN_FUNCTION_SIGNATURE = "\n\n[func signature]:\n{function_signature}\n\n[unit tests]:"

TEST_GEN_INSTRUCTION_AC = "You are a python coding assistant that answers in json format. Use the exact same structure as the example. Provide at least 1 basic and 1 edge test case."

TEST_GEN_FEW_SHOT_AC = '''
**Role**: As a tester, your task is to create comprehensive test cases for the incomplete `has_close_elements`
function. These test cases should encompass Basic, Edge, and Large Scale scenarios to ensure the code's
robustness, reliability, and scalability.
**1. Basic Test Cases**:
- **Objective**: To verify the fundamental functionality of the `has_close_elements` function under normal
conditions.
**2. Edge Test Cases**:
- **Objective**: To evaluate the function's behavior under extreme or unusual conditions.
**Instructions**:
- Implement a comprehensive set of test cases following the guidelines above.
- Ensure each test case is well-documented with comments explaining the scenario it covers.
- Pay special attention to edge cases as they often reveal hidden bugs.
**example start**
[func signature]:
```python
from typing import List
def has_close_elements(numbers: List[float], threshold: float) -> bool:
 """
 Check if in given list of numbers, are any two numbers closer to each other than given threshold.
 >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
 False
 >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
 True
 """
```
[unit tests]:
{{
  "basic": [
    {{
      "scenario": "Verify function with numbers close to each other within the threshold",
      "test": "assert has_close_elements([1.5, 2.0, 3.5], 0.6) == True"
    }},
    {{
      "scenario": "Verify function with numbers far from each other, exceeding the threshold",
      "test": "assert has_close_elements([1, 10, 20], 5) == False"
    }}
  ],
  "edge": [
    {{
      "scenario": "Test with an empty list",
      "test": "assert has_close_elements([], 5) == False"
    }},
    {{
      "scenario": "Test with a list containing only one element",
      "test": "assert has_close_elements([10], 5) == False"
    }}
  ]
}}

**example end**
**Task**:
'''

TEST_REFINEMENT_INSTRUCTION = "You are a Python programming assistant that can refine a given test case, given the function signature and the original test case. Provide a short explanation, if the test case is correct or incorrect. Provide the refined or original test case after your explanation, in the the format: python```assert <test>```"

TEST_REFINEMENT_PlACEHOLDER = """
[func signature]:
{function_signature}
[original test]:
{test}
[Explanation and refined test]:
"""

TEST_DETECTION_INSTRUCTION = "Given the following list of unit tests and the docstring for a specific function, check whether the ouput for each test is correct. Respond in the exact same json format as the example."

TEST_DETECTION_PLACEHOLDER = """
**Example**:
[func signature]:
from typing import List\n\n\ndef remove_duplicates(numbers: List[int]) -> List[int]:\n    \"\"\" From a list of integers, remove all elements that occur more than once.\n    Keep order of elements left the same as in the input.\n    >>> remove_duplicates([1, 2, 3, 2, 4])\n    [1, 3, 4]\n    \"\"\"\n
[generated tests]:
assert remove_duplicates([10, 20, 20, 10, 30]) == [10, 20, 30]
assert remove_duplicates([-1, -2, -2, -1, -3]) == [-1, -2, -3]
assert remove_duplicates([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
[response]:
{{
  tests: [
    {{
        "test": "assert remove_duplicates([10, 20, 20, 10, 30]) == [10, 20, 30]",
        "analysis": "The test expects duplicates to be reduced to a single instance, which conflicts with the function's design to remove all occurrences of duplicates.",
        "is_correct": false
    }},
    {{
        "test": "assert remove_duplicates([-1, -2, -2, -1, -3]) == [-1, -2, -3]",
        "analysis": "This test misunderstands the function's purpose. It expects a preservation of one instance of each number, whereas the function aims to eliminate all repeated numbers.",
        "is_correct": false
    }},
    {{
        "test": "assert remove_duplicates([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]",
        "analysis": "Since there are no duplicates in the input list, the function's output correctly matches the input list, aligning with the expected behavior.",
        "is_correct": true
    }}
  ]
}}
**Task**:
[func signature]:
{function_signature}
[generated tests]:
{tests}
[response]:
"""