TEST_GEN_CHAT_INSTRUCTION = """You are an AI coding assistant that can write unique, diverse, and intuitive unit tests for functions given the signature and docstring. Answer with code only not in English."""

TEST_GEN_FEW_SHOT = """Example:
func signature:
def add3Numbers(x, y, z):
    \"\"\" Add three numbers together.
    This function takes three numbers as input and returns the sum of the three numbers.
    \"\"\"
unit tests:
assert add3Numbers(1, 2, 3) == 6
assert add3Numbers(-1, 2, 3) == 4
assert add3Numbers(1, -2, 3) == 2
assert add3Numbers(1, 2, -3) == 0
assert add3Numbers(-3, -2, -1) == -6
assert add3Numbers(0, 0, 0) == 0
"""

TEST_GEN_FUNCTION_SIGNATURE = "\n\n[func signature]:\n{function_signature}\n\n[unit tests]:"

TEST_GEN_INSTRUCTION_AC = "You are a python coding assistant that answers in json format. Use the exact same structure as the example. Do not add or remove any keys."

TEST_GEN_FEW_SHOT_AC = '''
**Role**: As a tester, your task is to create comprehensive test cases for the incomplete `has_close_elements`
function. These test cases should encompass Basic, Edge, and Large Scale scenarios to ensure the code's
robustness, reliability, and scalability.
**1. Basic Test Cases**:
- **Objective**: To verify the fundamental functionality of the `has_close_elements` function under normal
conditions.
**2. Edge Test Cases**:
- **Objective**: To evaluate the function's behavior under extreme or unusual conditions.
**3. Large Scale Test Cases**:
- **Objective**: To assess the function’s performance and scalability with large data samples.
**Instructions**:
- Implement a comprehensive set of test cases following the guidelines above.
- Ensure each test case is well-documented with comments explaining the scenario it covers.
- Pay special attention to edge cases as they often reveal hidden bugs.
- For large-scale tests, focus on the function's efficiency and performance under heavy loads.
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
    "# Verify function with numbers close to each other within the threshold",
    "assert has_close_elements([1.5, 2.0, 3.5], 0.6) == True",
    "# Verify function with numbers far from each other, exceeding the threshold",
    "assert has_close_elements([1, 10, 20], 5) == False"
  ],
  "edge": [
    "# Test with an empty list",
    "assert has_close_elements([], 5) == False",
    "# Test with a list containing only one element",
    "assert has_close_elements([10], 5) == False"
  ],
  "large_scale": [
    "# Test with a very large list of numbers to assess performance",
    "assert has_close_elements(list(range(10000)), 0.5) == False",
    "# Corrected: Test with a large list where at least two elements are just within the threshold",
    "assert has_close_elements([i * 0.001 for i in range(10000)] + [0.0015], 0.0009) == True"
  ]
}}
**example end**
**Task**:
'''