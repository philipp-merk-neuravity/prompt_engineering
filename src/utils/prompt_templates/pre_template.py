SCOT_PSEUDOCODE_GEN_INSTRUCTION = '''You are a coding assistant that can write pseudocode only.'''

SCOT_PSEUDOCODE_GEN_FEW_SHOT = '''
**Example**:
[function_description]:
def first_Repeated_Char(str):
"""
Write a python function to find the first repeated
character in a given string.
"""

[instruction]:
Please understand the requirement and write a rough solving
process. It starts with a input-output structure. You
should use three basic structures to build the solving
process, including sequences, branches, and loops. The
necessary details should be written in natural languages.

[pseudocode]:
Input: str: a string
Output: ch: a repeated character in str
    for each character ch in str:
        if ch appears more than once in str:
            return ch
    return None
**Task**:
[function_description]:
{function_description}
[instruction]:
Please understand the requirement and write a rough solving
process. It starts with a input-output structure. You
should use three basic structures to build the solving
process, including sequences, branches, and loops. The
necessary details should be written in natural languages.
[pseudocode]:
'''

SYNTH_FEW_SHOT_GEN_INSTRUCTION_PRE = "Given a problem, explain the core concepts in it and provide three other relevant problems as shown in the example. Use json format for your response."

SYNTH_FEW_SHOT_GEN_FEW_SHOT_PRE = '''
Important: Do not forget to include imports at the key "code_solution" if necessary.
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
      "code_solution": "def reverse_string(s):\n    return s[::-1]"
    }}
  ],
}}
# Task:
[function_description]:
{function_description}
[response]:
'''
