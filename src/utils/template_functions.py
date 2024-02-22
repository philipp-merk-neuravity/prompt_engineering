from .prompt_templates.pre_template import (SCOT_PSEUDOCODE_GEN_INSTRUCTION, SCOT_PSEUDOCODE_GEN_FEW_SHOT)
from .prompt_templates.solution_template import (AC_CODE_GEN_INSTRUCTION, IO_CODE_GEN_FUNCTION_SIGNATURE, IO_CODE_GEN_FEW_SHOT, IO_CODE_GEN_INSTRUCTION, SCOT_CODE_GEN_FEW_SHOT, SCOT_CODE_GEN_INSTRUCTION, SYNTH_FEW_SHOT_GEN_FEW_SHOT, SYNTH_FEW_SHOT_GEN_INSTRUCTION)
from .prompt_templates.syntax_correction_template import (SYNTAX_CORRECTION_CODE_SOLUTION, SYNTAX_CORRECTION_FEEDBACK, SYNTAX_CORRECTION_INSTRUCTION)
from .prompt_templates.reflection_template import (SELF_REFLECTION_CHAT_INSTRUCTION, SELF_REFLECTION_CURRENT_FEEDBACK, SELF_REFLECTION_FEW_SHOT)
from .prompt_templates.refinement_template import (REFINEMENT_FEW_SHOT, REFINEMENT_FUNC_SIGNATURE, REFINEMENT_INSTRUCTION, REFINEMENT_PREVIOUS_FUNCTION_IMPL, REFINEMENT_REFLECTION, REFINEMENT_TESTS)
from .prompt_templates.tests_template import (TEST_GEN_CHAT_INSTRUCTION, TEST_GEN_FEW_SHOT, TEST_GEN_FUNCTION_SIGNATURE)

from .openai_api import create_system_message, create_user_message, create_ai_message

def get_messages_for_prompt_preprocessing(function_description: str, prompt_type="scot"):
    if prompt_type == "scot":
        return [
            create_system_message(SCOT_PSEUDOCODE_GEN_INSTRUCTION),
            create_user_message(SCOT_PSEUDOCODE_GEN_FEW_SHOT, function_description=function_description),
        ]

async def get_messages_for_code_generation(function_description: str, prompt_type="io", preprocessed_prompt=None):
    """
    Generates a sequence of messages intended for code generation tasks, based on the provided function signature and prompt type.

    This function prepares a list of system and user messages that are tailored to facilitate code generation, leveraging different prompting strategies. The prompt type determines the nature of the code generation request, supporting a variety of techniques from direct input/output examples to more complex few-shot learning scenarios.

    Parameters:
    - function_signature (str): The signature of the function to generate code for. This should include the function name and any parameters in a string format.
    - prompt_type (str): The type of prompt strategy to use for code generation. Supported values are:
        - 'io': Input/Output based prompting.
        - 'few_shot': Few-shot learning with examples.
        - 'synth_few_shot': Synthetic few-shot learning, using generated examples.
        - 'scot': Self-contained few-shot learning with explanations.
        - 'zero_shot_cot': Zero-shot learning with chain-of-thought prompting.
        - 'agentCoder': Agent-based approach to generate code.
      Defaults to 'io' if not specified.

    Returns:
    - A list of messages, where the first message is a system instruction for code generation, followed by a user message containing the function signature.
    """
    if prompt_type == "io":
        return [
            create_system_message(IO_CODE_GEN_INSTRUCTION),
            create_user_message(IO_CODE_GEN_FEW_SHOT + IO_CODE_GEN_FUNCTION_SIGNATURE, function_signature=function_description),
        ]
    if prompt_type == "few_shot":
        return ""
    if prompt_type == "synth_few_shot":
        return [
            create_system_message(SYNTH_FEW_SHOT_GEN_INSTRUCTION),
            create_user_message(SYNTH_FEW_SHOT_GEN_FEW_SHOT, function_description=function_description),
        ]
    if prompt_type == "scot":
        return [
            create_system_message(SCOT_CODE_GEN_INSTRUCTION),
            create_user_message(SCOT_CODE_GEN_FEW_SHOT, function_description=function_description, pseudo_code=preprocessed_prompt),
        ]
    if prompt_type == "zero_shot_cot":
        return ""
    if prompt_type == "agentCoder":
        return [
            create_system_message("You are a Python programming assistant that can answer with json format only."),
            create_user_message(AC_CODE_GEN_INSTRUCTION, function_description=function_description),
        ]
    
def get_messages_for_test_generation(function_signature: str):
    return [
        create_system_message(TEST_GEN_CHAT_INSTRUCTION),
        create_user_message(TEST_GEN_FEW_SHOT + TEST_GEN_FUNCTION_SIGNATURE, function_signature=function_signature),
    ]

def get_messages_for_self_reflection(function_implementation: str, unit_test_results: str):
    return [
        create_system_message(SELF_REFLECTION_CHAT_INSTRUCTION),
        create_user_message(SELF_REFLECTION_FEW_SHOT + SELF_REFLECTION_CURRENT_FEEDBACK, function_implementation=function_implementation, unit_test_results=unit_test_results),
    ]

def get_messages_for_refinement(function_signature: str, function_implementation: str, unit_test_results: str, reflection: str):
    return [
        create_system_message(REFINEMENT_INSTRUCTION),
        create_user_message(REFINEMENT_FEW_SHOT),
        create_ai_message(REFINEMENT_PREVIOUS_FUNCTION_IMPL, previous_implementation=function_implementation),
        create_user_message(REFINEMENT_TESTS, unit_test_results=unit_test_results),
        create_ai_message(REFINEMENT_REFLECTION, reflection_on_previous_implementation=reflection),
        create_user_message(REFINEMENT_FUNC_SIGNATURE, function_signature=function_signature),
    ]

def get_messages_for_syntax_correction(function_signature: str, code_solution: str, syntax_correction_feedback: str):
    return [
        create_system_message(SYNTAX_CORRECTION_INSTRUCTION),
        create_user_message(SYNTAX_CORRECTION_CODE_SOLUTION + SYNTAX_CORRECTION_FEEDBACK, function_signature=function_signature, code_solution=code_solution, syntax_correction_feedback=syntax_correction_feedback),
    ]