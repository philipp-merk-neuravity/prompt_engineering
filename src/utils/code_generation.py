from utils.openai_api import get_completion
from utils.prompt_templates import get_messages_for_syntax_correction, get_messages_for_code_generation, get_messages_for_refinement, get_messages_for_self_reflection, get_messages_for_test_generation
from utils.data_conversion import parse_code_block, convert_tests_to_list,add_imports_from_func_sig_to_code_solution, check_is_syntax_correct, split_tests_into_individual_functions, filter_syntactically_correct_tests_ast, remove_function_definition_from_test
import random
from typing import List

def get_syntactically_correct_code(code_solution: str, function_signature: str) -> str:
    is_syntax_correct, error_message = check_is_syntax_correct(code_solution)
    while not is_syntax_correct:
        messages = get_messages_for_syntax_correction(code_solution, error_message)
        code_solution = get_completion(messages)
        code_block = parse_code_block(code_solution)
        code_solution = add_imports_from_func_sig_to_code_solution(function_signature, code_block)
        is_syntax_correct, error_message = check_is_syntax_correct(code_solution)
    return code_solution

def gen_function(function_signature: str) -> str:
    messages = get_messages_for_code_generation(function_signature)
    code_solution = get_completion(messages)
    code_block = parse_code_block(code_solution)
    code_solution_with_imports = add_imports_from_func_sig_to_code_solution(function_signature, code_block)
    return get_syntactically_correct_code(code_solution_with_imports, function_signature)

def gen_tests(function_signature: str, amount=2) -> List[str]:
    messages = get_messages_for_test_generation(function_signature)
    tests = get_completion(messages, max_tokens=1024)
    tests_as_list = convert_tests_to_list(tests)
    tests_with_function_def = split_tests_into_individual_functions(tests_as_list)
    correct_tests_with_function_def = filter_syntactically_correct_tests_ast(tests_with_function_def)
    tests_as_list = [remove_function_definition_from_test(test) for test in correct_tests_with_function_def]
    return random.sample(tests_as_list, amount)

def gen_reflection(function_implementation: str, unit_test_results: str) -> str:
    messages = get_messages_for_self_reflection(function_implementation, unit_test_results)
    return get_completion(messages)

def gen_refined_function(function_signature: str, function_implementation: str, unit_test_results: str, reflection: str) -> str:
    messages = get_messages_for_refinement(function_signature, function_implementation, unit_test_results, reflection)
    refined_function = get_completion(messages)
    code_block = parse_code_block(refined_function)
    code_solution = add_imports_from_func_sig_to_code_solution(function_signature, code_block)
    return get_syntactically_correct_code(code_solution, function_signature)