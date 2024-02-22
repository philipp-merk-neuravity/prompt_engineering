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
