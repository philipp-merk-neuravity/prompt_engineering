from .prompt_templates.pre_template import (SYNTH_FEW_SHOT_GEN_INSTRUCTION_PRE, SYNTH_FEW_SHOT_GEN_FEW_SHOT_PRE, SCOT_PSEUDOCODE_GEN_INSTRUCTION, SCOT_PSEUDOCODE_GEN_FEW_SHOT)
from .prompt_templates.solution_template import (ZERO_SHOT_COT_PLACEHOLDER, ZERO_SHOT_COT_INSTRUCTION, AC_CODE_GEN_FEW_SHOT, AC_CODE_GEN_INSTRUCTION, SYNTH_FEW_SHOT_GEN_FEW_SHOT_POST, SYNTH_FEW_SHOT_GEN_INSTRUCTION_POST, IO_CODE_GEN_FUNCTION_SIGNATURE, IO_CODE_GEN_FEW_SHOT, IO_CODE_GEN_INSTRUCTION, SCOT_CODE_GEN_FEW_SHOT, SCOT_CODE_GEN_INSTRUCTION, SYNTH_FEW_SHOT_GEN_FEW_SHOT, SYNTH_FEW_SHOT_GEN_INSTRUCTION)
from .prompt_templates.syntax_correction_template import (SYNTAX_CORRECTION_CODE_SOLUTION, SYNTAX_CORRECTION_FEEDBACK, SYNTAX_CORRECTION_INSTRUCTION)
from .prompt_templates.reflection_template import (SELF_REFLECTION_CHAT_INSTRUCTION_2, SELF_REFLECTION_FEW_SHOT_2, SELF_REFLECTION_CHAT_INSTRUCTION, SELF_REFLECTION_CURRENT_FEEDBACK, SELF_REFLECTION_FEW_SHOT)
from .prompt_templates.refinement_template import (REFINEMENT_TASK, REFINEMENT_FEW_SHOT, REFINEMENT_FUNC_SIGNATURE, REFINEMENT_INSTRUCTION, REFINEMENT_PREVIOUS_FUNCTION_IMPL, REFINEMENT_REFLECTION, REFINEMENT_TESTS)
from .prompt_templates.tests_template import (TEST_GEN_CHAT_INSTRUCTION_SAVE, TEST_DETECTION_INSTRUCTION, TEST_DETECTION_PLACEHOLDER, TEST_REFINEMENT_INSTRUCTION, TEST_REFINEMENT_PlACEHOLDER, TEST_GEN_ZERO_SHOT_INSTRUCTION, TEST_GEN_INSTRUCTION_IO, TEST_GEN_CHAT_INSTRUCTION, TEST_GEN_FEW_SHOT, TEST_GEN_FUNCTION_SIGNATURE, TEST_GEN_FEW_SHOT_AC, TEST_GEN_INSTRUCTION_AC)

def create_system_message(template, **kwargs):
    return {"role": "system", "content": template.format(**kwargs)}

def create_user_message(template, **kwargs):
    return {"role": "user", "content": template.format(**kwargs)}

def create_ai_message(template, **kwargs):
    return {"role": "assistant", "content": template.format(**kwargs)}

async def get_messages_for_prompt_preprocessing(function_description: str, prompt_type="scot"):
    if prompt_type == "scot":
        return [
            create_system_message(SCOT_PSEUDOCODE_GEN_INSTRUCTION),
            create_user_message(SCOT_PSEUDOCODE_GEN_FEW_SHOT, function_description=function_description),
        ]
    if prompt_type == "synth_few_shot_split":
        return [
            create_system_message(SYNTH_FEW_SHOT_GEN_INSTRUCTION_PRE),
            create_user_message(SYNTH_FEW_SHOT_GEN_FEW_SHOT_PRE, function_description=function_description),
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
    if prompt_type == "synth_few_shot":
        return [
            create_system_message(SYNTH_FEW_SHOT_GEN_INSTRUCTION),
            create_user_message(SYNTH_FEW_SHOT_GEN_FEW_SHOT, function_description=function_description),
        ]
    if prompt_type == "synth_few_shot_split":
        return [
            create_system_message(SYNTH_FEW_SHOT_GEN_INSTRUCTION_POST),
            create_user_message(SYNTH_FEW_SHOT_GEN_FEW_SHOT_POST, function_description=function_description, preprocessed_prompt=preprocessed_prompt),
        ]
    if prompt_type == "scot":
        return [
            create_system_message(SCOT_CODE_GEN_INSTRUCTION),
            create_user_message(SCOT_CODE_GEN_FEW_SHOT, function_description=function_description, pseudo_code=preprocessed_prompt),
        ]
    if prompt_type == "zero_shot_cot":
        return [
            create_system_message(TEST_GEN_ZERO_SHOT_INSTRUCTION),
            create_user_message(TEST_GEN_FUNCTION_SIGNATURE, function_signature=function_description),
        ]
    
async def get_messages_for_test_generation(function_signature: str, prompt_type="io"):
    if prompt_type == "io":
        return [
            create_system_message(TEST_GEN_INSTRUCTION_IO),
            create_user_message(TEST_GEN_FUNCTION_SIGNATURE, function_signature=function_signature),
        ]
    if prompt_type == "few_shot":
        return [
            create_system_message(TEST_GEN_CHAT_INSTRUCTION_SAVE),
            create_user_message(TEST_GEN_FEW_SHOT + TEST_GEN_FUNCTION_SIGNATURE, function_signature=function_signature),
        ]
    if prompt_type == "zero_shot_cot":
        return [
            create_system_message(TEST_GEN_ZERO_SHOT_INSTRUCTION),
            create_user_message(TEST_GEN_FUNCTION_SIGNATURE, function_signature=function_signature),
        ]
    
async def get_messages_for_test_refinement(test: str, function_signature: str):
    return [
        create_system_message(TEST_REFINEMENT_INSTRUCTION),
        create_user_message(TEST_REFINEMENT_PlACEHOLDER, function_signature=function_signature, test=test),
    ]

async def get_messages_for_test_detection(tests: str, function_signature: str):
    return [
        create_system_message(TEST_DETECTION_INSTRUCTION),
        create_user_message(TEST_DETECTION_PLACEHOLDER, function_signature=function_signature, tests=tests),
    ]

async def get_messages_for_self_reflection(function_implementation: str, unit_test_results: str, prompt: str):
    if prompt == "reflexion":
        return [
            create_system_message(SELF_REFLECTION_CHAT_INSTRUCTION),
            create_user_message(SELF_REFLECTION_FEW_SHOT + SELF_REFLECTION_CURRENT_FEEDBACK, function_implementation=function_implementation, unit_test_results=unit_test_results),
        ]
    if prompt == "simple":
        return [
            create_system_message(SELF_REFLECTION_CHAT_INSTRUCTION),
            create_user_message(SELF_REFLECTION_CURRENT_FEEDBACK, function_implementation=function_implementation, unit_test_results=unit_test_results),
        ]

async def get_messages_for_refinement(function_signature: str, function_implementation: str, unit_test_results: str, reflection: str, prompt: str):
    if prompt == "reflexion":
        return [
            create_system_message(REFINEMENT_INSTRUCTION),
            create_user_message(REFINEMENT_FEW_SHOT),
            create_user_message(REFINEMENT_TASK, function_signature=function_signature),
            create_ai_message(REFINEMENT_PREVIOUS_FUNCTION_IMPL, previous_implementation=function_implementation),
            create_user_message(REFINEMENT_TESTS, unit_test_results=unit_test_results),
            create_ai_message(REFINEMENT_REFLECTION, reflection_on_previous_implementation=reflection),
            create_user_message(REFINEMENT_FUNC_SIGNATURE),
        ]
    if prompt == "simple":
        return [
            create_system_message(REFINEMENT_INSTRUCTION),
            create_user_message(REFINEMENT_TASK, function_signature=function_signature),
            create_ai_message(REFINEMENT_PREVIOUS_FUNCTION_IMPL, previous_implementation=function_implementation),
            create_user_message(REFINEMENT_TESTS, unit_test_results=unit_test_results),
            create_ai_message(REFINEMENT_REFLECTION, reflection_on_previous_implementation=reflection),
            create_user_message(REFINEMENT_FUNC_SIGNATURE),
        ]
    
async def get_messages_for_reflection_and_refinement(function_implementation: str, unit_test_results: str):
    return [
        create_system_message(SELF_REFLECTION_CHAT_INSTRUCTION_2),
        create_user_message(SELF_REFLECTION_FEW_SHOT_2, previous_implementation=function_implementation, unit_test_results=unit_test_results),
    ]

async def get_messages_for_syntax_correction(function_signature: str, code_solution: str, syntax_correction_feedback: str):
    return [
        create_system_message(SYNTAX_CORRECTION_INSTRUCTION),
        create_user_message(SYNTAX_CORRECTION_CODE_SOLUTION + SYNTAX_CORRECTION_FEEDBACK, function_signature=function_signature, code_solution=code_solution, syntax_correction_feedback=syntax_correction_feedback),
    ]