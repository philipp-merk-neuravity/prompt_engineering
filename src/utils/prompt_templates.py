from utils.openai_api import create_system_message, create_user_message, create_ai_message

programmers_prompt = '''
    **Instructions**:
    1. **Understand and Clarify**: Make sure you understand the task.
    2. **Algorithm/Method Selection**: Decide on the most efficient way.
    3. **Pseudocode Creation**: Write down the steps you will follow in pseudocode.
    4. **Code Generation**: Translate your pseudocode into executable Python code.
    **Few-Shot**:
    Task:
    \n\ndef strlen(string: str) -> int:\n    \"\"\" Return length of given string\n    >>> strlen('')\n    0\n    >>> strlen('abc')\n    3\n    \"\"\"\n
    1. **Understand and Clarify**:
   - The task is to implement a function that returns the length of a given string.
   - The length of a string is the number of characters it contains.
   - For example, the length of the string "hello" is 5.

    2. **Algorithm/Method Selection**:
    - Python provides a built-in function `len()` that returns the number of items in an object. When the object is a string, `len()` returns the number of characters in the string.
    - This task can be directly solved by using the `len()` function, making the implementation straightforward and efficient.

    3. **Pseudocode Creation**:
    ```
    function strlen(string):
        return the length of the string using the len() function
    ```

    4. **Code Generation**:
    ```python
    def strlen(string):
        """Return the length of the given string.
        >>> strlen('')
        0
        >>> strlen('abc')
        3
        """
        # Use the built-in len() function to find the length of the string.
        return len(string)
    ```
    Task:
    {function_description}
'''

CODE_GEN_INSTRUCTION = "You are an AI that only responds with python code, NOT ENGLISH. You will be given a function signature and its docstring by the user. Write your full implementation (restate the function signature)."

CODE_GEN_FEW_SHOT = "Use a Python code block to write your response. For example:\n```python\nprint('Hello world!')\n```\n"

CODE_GEN_FUNCTION_SIGNATURE = "{function_signature}"

def get_messages_for_code_generation(function_signature: str):
    return [
        create_system_message(CODE_GEN_INSTRUCTION + "\n" + CODE_GEN_FEW_SHOT),
        create_user_message(CODE_GEN_FUNCTION_SIGNATURE, function_signature=function_signature),
    ] 

TEST_GEN_CHAT_INSTRUCTION = """You are an AI coding assistant that can write unique, diverse, and intuitive unit tests for functions given the signature and docstring."""

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

def get_messages_for_test_generation(function_signature: str):
    return [
        create_system_message(TEST_GEN_CHAT_INSTRUCTION),
        create_user_message(TEST_GEN_FEW_SHOT + TEST_GEN_FUNCTION_SIGNATURE, function_signature=function_signature),
    ]

SELF_REFLECTION_CHAT_INSTRUCTION = "You are a Python programming assistant. You will be given a function implementation and a series of unit tests. Your goal is to write a few sentences to explain why your implementation is wrong as indicated by the tests. You will need this as a hint when you try again later. Only provide the few sentence description in your answer, not the implementation."

SELF_REFLECTION_FEW_SHOT = """Example 1:
[function impl]:
```python
def longest_subarray_with_sum_limit(nums: List[int], target: int) -> List[int]:
    n = len(nums)
    left, right = 0, 0
    max_length = 0
    current_sum = 0
    result = []
    while right < n:
        current_sum += nums[right]
        while current_sum > target:
            current_sum -= nums[left]
            left += 1
        if right - left + 1 >= max_length:
            max_length = right - left + 1
            result = nums[left:right+1]
        right += 1
    return result
```
[unit test results]:
Tests passing:
assert longest_subarray_with_sum_limit([1, 2, 3, 4, 5], 8) == [1, 2, 3]
assert longest_subarray_with_sum_limit([1, 2, 3, 4, 5], 15) == [1, 2, 3, 4, 5]
assert longest_subarray_with_sum_limit([1, -1, 2, -2, 3, -3], 2) == [1, -1, 2, -2, 3]
assert longest_subarray_with_sum_limit([], 10) == []
assert longest_subarray_with_sum_limit([], 0) == []
assert longest_subarray_with_sum_limit([], -5) == []  
Tests failing:
assert longest_subarray_with_sum_limit([5, 6, 7, 8, 9], 4) == [] # output: [5]
[self-reflection]:
The implementation failed the where no subarray fulfills the condition. The issue in the implementation is due to the use of >= instead of > in the condition to update the result. Because of this, it returns a subarray even when the sum is greater than the target, as it still updates the result when the current subarray length is equal to the previous longest subarray length. To overcome this error, we should change the condition to only update the result when the current subarray length is strictly greater than the previous longest subarray length. This can be done by replacing >= with > in the condition.

Example 2:
[function impl]:
```python
def longest_subarray_with_sum_limit(nums: List[int], target: int) -> List[int]:
    n = len(nums)
    left, right = 0, 0
    max_length = 0
    current_sum = 0
    result = []
    while current_sum + nums[right] <= target:
        current_sum += nums[right]
        right += 1
    while right < n:
        current_sum += nums[right]
        while current_sum > target:
            current_sum -= nums[left]
            left += 1
        if right - left + 1 > max_length:
            max_length = right - left + 1
            result = nums[left:right+1]
        right += 1
    return result
```
[unit test results]:
Tests passing:
assert longest_subarray_with_sum_limit([], 10) == []
assert longest_subarray_with_sum_limit([], 0) == []
assert longest_subarray_with_sum_limit([], -5) == []
Tests failing:
assert longest_subarray_with_sum_limit([1, 2, 3, 4, 5], 8) == [1, 2, 3] # output: list index out of range
assert longest_subarray_with_sum_limit([1, 2, 3, 4, 5], 15) == [1, 2, 3, 4, 5] # output: list index out of range
assert longest_subarray_with_sum_limit([5, 6, 7, 8, 9], 4) == [] # output: list index out of range
assert longest_subarray_with_sum_limit([1, -1, 2, -2, 3, -3], 2) == [1, -1, 2, -2, 3] # output: list index out of range
[self-reflection]:
The implementation failed 4 out of the 7 test cases due to an IndexError. The issue stems from the while loop while current_sum + nums[right] <= target:, which directly accesses nums[right] without checking if right is within the bounds of the list. This results in a runtime error when right goes beyond the list length. To overcome this error, we need to add a bounds check for the right variable in the mentioned while loop. We can modify the loop condition to while right < len(nums) and current_sum + nums[right] <= target:. This change will ensure that we only access elements within the bounds of the list, thus avoiding the IndexError.
END OF EXAMPLES
"""

SELF_REFLECTION_CURRENT_FEEDBACK = "\n\n[function impl]:\n```python\n{function_implementation}\n```\n\n[unit test results]:\n{unit_test_results}\n\n[self-reflection]:"

def get_messages_for_self_reflection(function_implementation: str, unit_test_results: str):
    return [
        create_system_message(SELF_REFLECTION_CHAT_INSTRUCTION),
        create_user_message(SELF_REFLECTION_FEW_SHOT + SELF_REFLECTION_CURRENT_FEEDBACK, function_implementation=function_implementation, unit_test_results=unit_test_results),
    ] 

REFINEMENT_INSTRUCTION = "You are an AI Python assistant. You will be given your past function implementation, a series of unit tests, and a hint to change the implementation appropriately. Write your full implementation (restate the function signature).\nUse a Python code block to write your response. For example:\n```python\nprint('Hello world!')\n```"

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
assert add(1, 2) == 3 # output: -1
assert add(1, 2) == 4 # output: -1

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

REFINEMENT_PREVIOUS_FUNCTION_IMPL = "```python\n{previous_implementation}\n```"
REFINEMENT_TESTS = "[unit test results from previous impl]:\n{unit_test_results}\n\n[reflection on previous impl]"
REFINEMENT_REFLECTION = "{reflection_on_previous_implementation}"
REFINEMENT_FUNC_SIGNATURE = "[improved impl]:\n{function_signature}"

def get_messages_for_refinement(function_signature: str, function_implementation: str, unit_test_results: str, reflection: str):
    return [
        create_system_message(REFINEMENT_INSTRUCTION),
        create_user_message(REFINEMENT_FEW_SHOT),
        create_ai_message(REFINEMENT_PREVIOUS_FUNCTION_IMPL, previous_implementation=function_implementation),
        create_user_message(REFINEMENT_TESTS, unit_test_results=unit_test_results),
        create_ai_message(REFINEMENT_REFLECTION, reflection_on_previous_implementation=reflection),
        create_user_message(REFINEMENT_FUNC_SIGNATURE, function_signature=function_signature),
    ]

# Syntax Correction

SYNTAX_CORRECTION_INSTRUCTION = "You are an AI that only responds with python code, NOT ENGLISH. You will be given a code snippet with a syntax error. Your goal is to correct the syntax error in the code snippet. Write the corrected code snippet.\nUse a Python code block to write your response. For example:\n```python\nprint('Hello world!')\n```"
SYNTAX_CORRECTION_CODE_SOLUTION = "[impl]```python\n{code_solution}\n```\n\n"
SYNTAX_CORRECTION_FEEDBACK = "{syntax_correction_feedback}\n\n[improved impl]:"

def get_messages_for_syntax_correction(code_solution: str, syntax_correction_feedback: str):
    return [
        create_system_message(SYNTAX_CORRECTION_INSTRUCTION),
        create_user_message(SYNTAX_CORRECTION_CODE_SOLUTION + SYNTAX_CORRECTION_FEEDBACK, code_solution=code_solution, syntax_correction_feedback=syntax_correction_feedback),
    ]