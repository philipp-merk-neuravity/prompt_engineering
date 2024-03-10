REFINEMENT_INSTRUCTION = "You are an AI Python assistant that can only answer with python code not english. You will be given your past function implementation, a series of unit tests, and a hint to change the implementation appropriately. Write your full implementation (restate the function signature).\nUse a Python code block to write your response. For example:\npython```\n def greet(name):    return f'Hello, {{name}}!'```. Do not add unit tests, e.g. this would be wrong: \npython```def greet(name):    return f'Hello, {{name}}!'\nassert greet('world') == 'Hello, world!', 'The greeting did not match the expected output.'```. Please include the function signature and import statements."


REFINEMENT_FEW_SHOT = '''Example 1:
[previous impl]:
```python
def add(a: int, b: int) -> int:
    """
    Given integers a and b, return the total value of a and b.
    """
    return a - b
```

[unit test results from previous impl]:
Tested passed:

Tests failed:
[assert add(1, 2) == 3 # output: -1,
assert add(1, 2) == 4 # output: -1]

[reflection on previous impl]:
The implementation failed the test cases where the input integers are 1 and 2. The issue arises because the code does not add the two integers together, but instead subtracts the second integer from the first. To fix this issue, we should change the operator from `-` to `+` in the return statement. This will ensure that the function returns the correct output for the given input.

[improved impl]:
```python
def add(a: int, b: int) -> int:
    """
    Given integers a and b, return the total value of a and b.
    """
    return a + b
```
'''
REFINEMENT_TASK = "[task]:\n{function_signature}"
REFINEMENT_PREVIOUS_FUNCTION_IMPL = "[previous impl]:\n```python\n{previous_implementation}\n```"
REFINEMENT_TESTS = "[unit test results from previous impl]:\n{unit_test_results}\n\n[reflection on previous impl]:\n"
REFINEMENT_REFLECTION = "{reflection_on_previous_implementation}\n\n"
REFINEMENT_FUNC_SIGNATURE = "Do NOT add Test cases to your response. This would be wrong: 'def sort_third(l: list):\n    return [sorted(l[i]) if i % 3 == 0 else l[i] for i in range(len(l))]\n\n# Test cases\nprint(sort_third([1, 2, 3]))\nprint(sort_third([5, 6, 3, 4, 8, 9, 2]))'. This would be correct: 'def sort_third(l: list):\n    return [sorted(l[i]) if i % 3 == 0 else l[i] for i in range(len(l))]'[improved impl]:"
