# start-prompt -> unit test -> reflexion -> refine prompt
from utils.code_generation import gen_function, gen_tests
from utils.load_benchmark import load_benchmark
from utils.prompt_templates import get_prompt_template_for_code_generation, get_prompt_template_for_test_generation
from utils.execute_tests import get_test_results
import json

humanEval_data = load_benchmark()
prompt_template_for_code_generation = get_prompt_template_for_code_generation()
prompt_template_for_test_generation = get_prompt_template_for_test_generation()

def run_test_gen():
    generated_tests = []
    for item in humanEval_data[:2]: 
        function_signature = item["prompt"]
        generated_tests.append(gen_tests(prompt_template_for_test_generation, function_signature))
    return generated_tests

def run_reflexion():
    results = []
    is_solved = False
    for item in humanEval_data[:2]: 
        item_copy = item.copy()
        function_signature = item["prompt"]
        unit_tests = gen_tests(prompt_template_for_test_generation, function_signature)
        generated_code = gen_function(prompt_template_for_code_generation, function_signature)
        test_results, current_is_solved = get_test_results(generated_code, unit_tests)
        item_copy["generated_solution"] = generated_code
        item_copy["test_results"] = test_results
        is_solved = current_is_solved
        results.append(item_copy)
    return results

# benchmark_results = run_benchmark()  
test_results = run_reflexion()
print(test_results)