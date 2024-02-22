
SCOT_CODE_GEN_INSTRUCTION="""You will be given a function description and pseudocode. Solve the task with python code only, not natural language."""

SCOT_CODE_GEN_FEW_SHOT='''
[function_description]:
{function_description}
[pseudo_code]:
{pseudo_code}
[code_solution]:
'''

AC_CODE_GEN_INSTRUCTION = '''
    Generate a json object with the exact same structure given in the example.

    1. understand_and_clarify: Make sure you understand the task.
    2. method_selection: Decide on the most efficient way.
    3. pseudo_code: Write down the steps you will follow in pseudocode.
    4. code_generation: Translate your pseudocode into executable Python code. Do not forget to add imports if necessary. The key code_solution has not subkeys. 
    Example Task:
    [function_description]: \n\ndef strlen(string: str) -> int:\n    \"\"\" Return length of given string\n    >>> strlen('')\n    0\n    >>> strlen('abc')\n    3\n    \"\"\"\n
    [response]:
    {{
      "understand_and_clarify": {{
        "task": "Implement a function that returns the length of a given string.",
        "string_length_definition": "The length of a string is the number of characters it contains.",
        "example": "For example, the length of the string 'hello' is 5."
      }},
      "method_selection": {{
        "description": "Python provides a built-in function 'len()' that returns the number of items in an object. When the object is a string, 'len()' returns the number of characters in the string.",
        "rationale": "This task can be directly solved by using the 'len()' function, making the implementation straightforward and efficient."
      }},
      "pseudocode": "function strlen(string):\n    return the length of the string using the len() function",
      "code_solution": "def strlen(string):\n    return len(string)"
    }}
    Task:
    [function_description]:
    {function_description}
    [response]:
'''

IO_CODE_GEN_INSTRUCTION = "Solve the coding task. Respond with python code only, not english. Restate the function signature."

IO_CODE_GEN_FEW_SHOT = "Use a python code block, e.g.:\n```python\ndef foo():    print('Hello world!')\n```\n"

IO_CODE_GEN_FUNCTION_SIGNATURE = "{function_signature}"

SYNTH_FEW_SHOT_GEN_INSTRUCTION = "Your goal is to write Python3 code to solve competitive programming problems. Given a problem, explain the core concepts in it and provide three other relevant problems. Then solve the original problem. Use syntactically correct json format for your response."

SYNTH_FEW_SHOT_GEN_FEW_SHOT = '''
Important: Do not forget to include imports at the key "Python3 Code" if necessary.
# Example:
[function_description]:
\n\ndef strlen(string: str) -> int:\n    \"\"\" Return length of given string\n    >>> strlen('')\n    0\n    >>> strlen('abc')\n    3\n    \"\"\"\n
[response]: 
{{
  "Algorithms": "String Manipulation",
  "Tutorial": "In Python, strings are arrays of bytes representing Unicode characters. We can access elements of the string using square brackets. The built-in len() function is used to find the length of the string.",
  "Example Problems": [
    {{
      "Problem Description": "Write a function to reverse a string.",
      "Solution Explanation": "We can create a new string that's a reversed version of the input string by slicing it with a step of -1.",
      "Python3 Code": "def reverse_string(s):\n    return s[::-1]"
    }}
  ],
  "Original Problem Solution": {{
    "Explanation": "The built-in len() function returns the number of characters in the string.",
    "Python3 Code": "def strlen(string: str) -> int:\n    return len(string)"
  }}
}}
# Task:
[function_description]:
{function_description}
[response]:
'''
