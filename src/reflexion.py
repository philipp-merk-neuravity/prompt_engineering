# start-prompt -> unit test -> reflexion -> refine prompt
# 1. Create a file with fields: task_id, completion for evaluation
# 2. Test this approach for 20 tasks
# 3. Check if the implementation passes the tests, if not 
# 4. Refine the prompt -> reflexion prompt + execution -> refinement prompt + execution
# 5. use a loop to refine the prompt and execute the code
# 6. If it passes the tests, then it is solved and can be written to the file
from utils.code_generation import gen_function, gen_tests, gen_reflection, gen_refined_function
from utils.storage import load_benchmark, save_benchmark_results, load_benchmark_results
from utils.test_execution import get_test_results
from utils.data_conversion import  convert_unit_test_results_to_str

humanEval_data = load_benchmark()
benchmark_results = load_benchmark_results()
humanEval_data_unsolved = [item for item in humanEval_data if item["task_id"] not in [result["task_id"] for result in benchmark_results]]

def run_reflection(max_iterations=2):
    for item in humanEval_data_unsolved: 
        print(item["task_id"])
        current_iteration = 0
        function_signature = item["prompt"]

        generated_tests = gen_tests(function_signature)
        generated_code = gen_function(function_signature)
        test_results, is_solved = get_test_results(generated_code, generated_tests)
        
        if (is_solved):
            save_benchmark_results(item["task_id"], generated_code)
            continue

        while ((current_iteration < max_iterations) and not is_solved):
            unit_test_results_as_str = convert_unit_test_results_to_str(test_results)
            
            reflexion = gen_reflection(generated_code, unit_test_results_as_str)
            generated_code = gen_refined_function(function_signature, generated_code, unit_test_results_as_str, reflexion)
            test_results, is_solved = get_test_results(generated_code, generated_tests)

            if (is_solved or current_iteration == max_iterations - 1):
                save_benchmark_results(item["task_id"], generated_code)
                break

            current_iteration += 1

run_reflection()