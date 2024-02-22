
SYNTAX_CORRECTION_INSTRUCTION = "You are an AI that only responds with python code, NOT ENGLISH. You will be given a function description and the code solution with a syntax error. Your goal is to correct the syntax error in the code solution. Restate the function signature."
SYNTAX_CORRECTION_CODE_SOLUTION = "[function_description]: {function_signature}\n\n[impl]```python\n{code_solution}\n```\n\n"
SYNTAX_CORRECTION_FEEDBACK = "[syntax_errors]: {syntax_correction_feedback}\n\n[improved impl]:"
