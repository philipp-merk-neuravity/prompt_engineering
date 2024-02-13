from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage

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

CODE_GEN_FUNCTION_SIGNATURE = "[func_sig]:{function_signature}"

def get_prompt_template_for_code_generation():
    return ChatPromptTemplate.from_messages(
    [
        SystemMessage(CODE_GEN_INSTRUCTION),
        HumanMessagePromptTemplate.from_template(CODE_GEN_FEW_SHOT +  CODE_GEN_FUNCTION_SIGNATURE)
    ]
)

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
\n\n[func signature]:\n{function_signature}\n\n[unit tests]:
"""

def get_prompt_template_for_test_generation():
    return ChatPromptTemplate.from_messages(
    [
        SystemMessage(TEST_GEN_CHAT_INSTRUCTION),
        HumanMessagePromptTemplate.from_template(TEST_GEN_FEW_SHOT)
    ]
)