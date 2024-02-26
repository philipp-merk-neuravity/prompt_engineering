from .openai_api import get_completion
from .template_functions import get_messages_for_reflection_and_refinement, get_messages_for_refinement, get_messages_for_code_generation, get_messages_for_syntax_correction, get_messages_for_test_generation, get_messages_for_prompt_preprocessing, get_messages_for_self_reflection
from .data_conversion import convert_unit_test_results_to_str, extract_python_code_from_json, parse_code_block, convert_tests_to_list, check_is_syntax_correct, split_tests_into_individual_functions, filter_syntactically_correct_tests_ast, remove_function_definition_from_test
import random
from typing import List

async def evaluate_syntax_for_code_solution(code_solution: str, function_signature: str) -> str:
    is_syntax_correct, error_message = check_is_syntax_correct(code_solution)
    prompt_tokens_all = 0
    completion_tokens_all = 0
    duration_for_syntax_correction = 0
    while not is_syntax_correct:
        messages = await get_messages_for_syntax_correction(function_signature, code_solution, error_message)
        code_solution, prompt_tokens, completion_tokens, duration = await get_completion(messages)
        duration_for_syntax_correction += duration
        prompt_tokens_all += prompt_tokens
        completion_tokens_all += completion_tokens
        code_solution = parse_code_block(code_solution)
        is_syntax_correct, error_message = check_is_syntax_correct(code_solution)
    return code_solution, prompt_tokens_all, completion_tokens_all, duration_for_syntax_correction

async def gen_preprocessed_prompt(function_signature: str, prompt_type: str) -> str:
    messages = await get_messages_for_prompt_preprocessing(function_signature, prompt_type)
    return await get_completion(messages)

async def gen_function(function_description: str, model="gpt-3.5-turbo", prompt_type="io", preprocessed_prompt=None) -> tuple:
    response_format = "text"
    if prompt_type == "synth_few_shot" or prompt_type == "agentCoder":
        response_format = "json_object"
    messages = await get_messages_for_code_generation(function_description, prompt_type, preprocessed_prompt)
    response, prompt_tokens, completion_tokens, duration = await get_completion(messages, model=model, response_format=response_format)
    if prompt_type == "synth_few_shot" or prompt_type == "agentCoder":
        response = extract_python_code_from_json(response, prompt_type)
    code_block = parse_code_block(response)
    code_block, prompt_tokens_for_syntax_correction, completion_tokens_for_syntax_correction, duration_for_syntax_correction = await evaluate_syntax_for_code_solution(code_block, function_description)
    return (
        code_block,
        prompt_tokens + prompt_tokens_for_syntax_correction, 
        completion_tokens + completion_tokens_for_syntax_correction, 
        duration + duration_for_syntax_correction
    )

def gen_tests(function_signature: str, amount=1) -> List[str]:
    messages = get_messages_for_test_generation(function_signature)
    tests = get_completion(messages, max_tokens=4096)
    tests_as_list = convert_tests_to_list(tests)
    tests_with_function_def = split_tests_into_individual_functions(tests_as_list)
    correct_tests_with_function_def = filter_syntactically_correct_tests_ast(tests_with_function_def)
    tests_as_list = [remove_function_definition_from_test(test) for test in correct_tests_with_function_def]
    return random.sample(tests_as_list, amount)

async def gen_reflection(function_implementation: str, unit_test_results: str, model: str, prompt: str) -> str:
    messages = await get_messages_for_self_reflection(function_implementation, unit_test_results, prompt)
    return await get_completion(messages, model=model)

async def gen_refined_function(function_signature: str, function_implementation: str, unit_test_results: str, reflection: str, model: str, prompt: str) -> str:
    messages = await get_messages_for_refinement(function_signature, function_implementation, unit_test_results, reflection, prompt)
    refined_function, prompt_tokens, completion_tokens, duration = await get_completion(messages, model=model)
    code_block = parse_code_block(refined_function)
    code_block, prompt_tokens_for_syntax_correction, completion_tokens_for_syntax_correction, duration_for_syntax_correction = await evaluate_syntax_for_code_solution(code_block, function_signature)
    return (
        code_block,
        prompt_tokens + prompt_tokens_for_syntax_correction,
        completion_tokens + completion_tokens_for_syntax_correction,
        duration + duration_for_syntax_correction
    )

async def gen_reflection_and_refined_function(function_signature: str, function_implementation: str, unit_test_results: str, model: str) -> str:
    messages = await get_messages_for_reflection_and_refinement(function_implementation, unit_test_results)
    reflection_and_refined_function, prompt_tokens, completion_tokens, duration = await get_completion(messages, model=model, response_format="json_object")
    refined_function = extract_python_code_from_json(reflection_and_refined_function, "reflection_and_refinement")
    code_block = parse_code_block(refined_function)
    code_block, prompt_tokens_for_syntax_correction, completion_tokens_for_syntax_correction, duration_for_syntax_correction = await evaluate_syntax_for_code_solution(code_block, function_signature)
    return (
        code_block,
        prompt_tokens + prompt_tokens_for_syntax_correction,
        completion_tokens + completion_tokens_for_syntax_correction,
        duration + duration_for_syntax_correction
    )
