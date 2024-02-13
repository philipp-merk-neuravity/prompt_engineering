# start-prompt -> unit test -> reflexion -> refine prompt
# 1. Create a file with fields: task_id, completion for evaluation
# 2. Test this approach for 20 tasks
# 3. Check if the implementation passes the tests, if not 
# 4. Refine the prompt -> reflexion prompt + execution -> refinement prompt + execution
# 5. use a loop to refine the prompt and execute the code
# 6. If it passes the tests, then it is solved and can be written to the file
from utils.code_generation import gen_function, gen_tests, gen_reflection, gen_refined_function
from utils.storage import load_benchmark, save_benchmark_results
from utils.prompt_templates import get_prompt_template_for_code_generation, get_prompt_template_for_test_generation, get_prompt_template_for_self_reflection, get_prompt_template_for_reflexion
from utils.test_execution import get_test_results
from utils.data_conversion import extract_function_body, convert_unit_test_results_to_str

humanEval_data = load_benchmark()
prompt_template_for_code_generation = get_prompt_template_for_code_generation()
prompt_template_for_test_generation = get_prompt_template_for_test_generation()
prompt_template_for_self_reflection = get_prompt_template_for_self_reflection()
prompt_template_for_reflexion = get_prompt_template_for_reflexion()

def run_test_gen():
    generated_tests = []
    for item in humanEval_data[:2]: 
        function_signature = item["prompt"]
        generated_tests.append(gen_tests(prompt_template_for_test_generation, function_signature))
    return generated_tests

def run_reflexion(max_iterations=2):
    for item in humanEval_data[:2]: 
        current_iteration = 0
        current_is_solved = False
        function_signature = item["prompt"]

        generated_tests = gen_tests(prompt_template_for_test_generation, function_signature)

        generated_code = gen_function(prompt_template_for_code_generation, function_signature)
        
        test_results, is_solved = get_test_results(generated_code, generated_tests)
        current_is_solved = is_solved
        if (current_is_solved):
            save_benchmark_results(item["task_id"], generated_code)
            break
        
        current_iteration += 1
        unit_test_results_as_str = convert_unit_test_results_to_str(test_results)
        while (current_iteration < max_iterations and not current_is_solved):
            code_solution_body = extract_function_body(generated_code)
            function_implementation = f"{function_signature}\n{code_solution_body}"
            reflexion = gen_reflection(prompt_template_for_self_reflection, function_implementation, unit_test_results_as_str)
            generated_code = gen_refined_function(prompt_template_for_reflexion, function_signature, function_implementation, unit_test_results_as_str, reflexion)
            
            test_results, is_solved = get_test_results(generated_code, generated_tests)
            unit_test_results_as_str = convert_unit_test_results_to_str(test_results)
            current_is_solved = is_solved
            if (current_is_solved):
                save_benchmark_results(item["task_id"], generated_code)
                break

            current_iteration += 1


# benchmark_results = run_benchmark()  
test_results = run_reflexion()
print(test_results)