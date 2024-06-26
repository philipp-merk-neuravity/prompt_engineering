from .openai_api import get_completion
from .template_functions import get_messages_for_test_detection, get_messages_for_test_refinement, get_messages_for_reflection_and_refinement, get_messages_for_refinement, get_messages_for_code_generation, get_messages_for_syntax_correction, get_messages_for_test_generation, get_messages_for_prompt_preprocessing, get_messages_for_self_reflection
from .data_conversion import extract_function_name, extract_python_code_from_json, parse_code_block, convert_tests_to_list, check_is_syntax_correct, split_tests_into_individual_functions, filter_syntactically_correct_tests_ast, remove_function_definition_from_test
import random
from typing import List
import json

async def evaluate_syntax_for_code_solution(code_solution: str, function_signature: str) -> str:
    is_syntax_correct, error_message = check_is_syntax_correct(code_solution)
    prompt_tokens_all = 0
    completion_tokens_all = 0
    duration_for_syntax_correction = 0
    iteration = 0
    while not is_syntax_correct and iteration < 5:
        messages = await get_messages_for_syntax_correction(function_signature, code_solution, error_message)
        code_solution, prompt_tokens, completion_tokens, duration = await get_completion(messages, temperature=0.8)
        duration_for_syntax_correction += duration
        prompt_tokens_all += prompt_tokens
        completion_tokens_all += completion_tokens
        code_solution = parse_code_block(code_solution)
        is_syntax_correct, error_message = check_is_syntax_correct(code_solution)
        iteration += 1
        print(iteration)
    return code_solution, prompt_tokens_all, completion_tokens_all, duration_for_syntax_correction

async def gen_preprocessed_prompt(function_signature: str, prompt_type: str) -> str:
    messages = await get_messages_for_prompt_preprocessing(function_signature, prompt_type)
    return await get_completion(messages)

async def gen_function(function_description: str, model="gpt-3.5-turbo", prompt_type="io", preprocessed_prompt=None, temperature=0.2) -> tuple:
    response_format = "text"
    if prompt_type == "synth_few_shot" or prompt_type == "agentCoder":
        response_format = "json_object"
    messages = await get_messages_for_code_generation(function_description, prompt_type, preprocessed_prompt)
    response, prompt_tokens, completion_tokens, duration = await get_completion(messages, model=model, response_format=response_format, temperature=temperature)
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

async def remove_flawed_tests(tests: List[str], model: str, function_signature: str) -> List[str]:
    tests_as_str = "\n".join(tests)
    messages = await get_messages_for_test_detection(tests_as_str, function_signature)
    refined_tests, prompt_tokens, completion_tokens, duration = await get_completion(messages, model=model, response_format="json_object")

    refined_tests_as_json = json.loads(refined_tests)["tests"]

    refined_tests = [case['test'] for case in refined_tests_as_json if case['is_correct']]

    tests_with_function_def = split_tests_into_individual_functions(refined_tests)
    correct_tests_with_function_def = filter_syntactically_correct_tests_ast(tests_with_function_def)
    tests_as_list = [remove_function_definition_from_test(test) for test in correct_tests_with_function_def]

    return tests_as_list, prompt_tokens, completion_tokens, duration

async def gen_tests(function_signature: str, model: str, prompt_type: str, amount=4, response_format="text", model_for_refinement="gpt-4-0125-preview", use_refinement=False, temperature=0.2) -> List[str]:
    function_name = extract_function_name(function_signature)
    if prompt_type == "synth_few_shot":
        response_format = "json_object"
        messages_pre = await get_messages_for_test_generation(function_signature, "synth_few_shot_pre")
        preprocessed_prompt = await get_completion(messages_pre, response_format=response_format)
        response_format = "text"
        messages = await get_messages_for_test_generation(function_signature, prompt_type, function_name, preprocessed_prompt)
        tests, prompt_tokens, completion_tokens, duration = await get_completion(messages, model=model, response_format=response_format, temperature=temperature)
    else:    
        messages = await get_messages_for_test_generation(function_signature, prompt_type, function_name)
        tests, prompt_tokens, completion_tokens, duration = await get_completion(messages, max_tokens=4096, model=model, response_format=response_format, temperature=temperature)
    tests_as_list = convert_tests_to_list(tests, prompt_type)
    tests_with_function_def = split_tests_into_individual_functions(tests_as_list)
    correct_tests_with_function_def = filter_syntactically_correct_tests_ast(tests_with_function_def)
    tests_as_list = [remove_function_definition_from_test(test) for test in correct_tests_with_function_def]
    if amount < len(tests_as_list):
        tests_as_list = random.sample(tests_as_list, amount)
    if use_refinement:
        tests_as_list, prompt_tokens_filter, completion_tokens_filter, duration_filter = await remove_flawed_tests(tests_as_list, model_for_refinement, function_signature)
        return (tests_as_list, prompt_tokens, completion_tokens, duration, prompt_tokens_filter, completion_tokens_filter, duration_filter)
    return (tests_as_list, prompt_tokens, completion_tokens, duration)

async def gen_reflection(function_implementation: str, unit_test_results: str, model: str, prompt: str, temperature: str) -> str:
    messages = await get_messages_for_self_reflection(function_implementation, unit_test_results, prompt)
    return await get_completion(messages, model=model, temperature=temperature)

async def gen_refined_function(function_signature: str, function_implementation: str, unit_test_results: str, reflection: str, model: str, prompt: str, temperature: str) -> str:
    messages = await get_messages_for_refinement(function_signature, function_implementation, unit_test_results, reflection, prompt)
    refined_function, prompt_tokens, completion_tokens, duration = await get_completion(messages, model=model, temperature=temperature)
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
