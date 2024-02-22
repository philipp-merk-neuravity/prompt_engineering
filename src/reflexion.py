# params: max_iterations, model_per_task, tests

import asyncio
import argparse
from utils.code_generation import gen_function, gen_tests, gen_reflection, gen_refined_function
from utils.storage import load_benchmark, save_benchmark_results, load_benchmark_results
from utils.test_execution import get_test_results
from utils.data_conversion import  convert_unit_test_results_to_str
from typing import List


async def process_chunk(chunk, model, prompt_type):
    tasks = [gen_function(item["prompt"], model, prompt_type) for item in chunk]
    return await asyncio.gather(*tasks)

def convert_str_to_assert_list(input_str, new_function_name):
    """
    This function takes a string containing Python code and a new function name.
    It extracts all assert statements, replacing the original function name with the new one,
    and returns them as a list of strings.
    """
    # Extract assert statements and replace the function name
    assert_statements = [
        line.strip().replace('candidate', new_function_name) for line in input_str.split('\n') if line.strip().startswith('assert')
    ]
    return assert_statements

def load_test_cases(tests_path):
    with open(tests_path, 'r') as file:
        return file.read()

async def main(model_for_init, model_for_reflection, model_for_refinement, add_gpt4_on_round, max_iterations, benchmark_type, chunk_size, delay_seconds, tests_path):
    benchmark_data = load_benchmark(benchmark_type)
    test_cases = load_test_cases(tests_path)
    items_to_save = []
    for item in benchmark_data:
        current_iteration = 0
        function_signature = item["prompt"]

        generated_code = gen_function(function_signature)
        test_results, is_solved = get_test_results(generated_code, test_cases)
        
        if (is_solved):
            save_benchmark_results(item["task_id"], generated_code, test_cases)
            continue
    
        while True:
            unit_test_results_as_str = convert_unit_test_results_to_str(test_results)
             
            reflexion = gen_reflection(generated_code, unit_test_results_as_str)
            generated_code = gen_refined_function(function_signature, generated_code, unit_test_results_as_str, reflexion)
            test_results, is_solved = get_test_results(generated_code, test_cases)

            if (is_solved or current_iteration == max_iterations - 1):
                save_benchmark_results(item["task_id"], generated_code, test_cases)
                break

            current_iteration += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run async tasks with model parameter.')
    parser.add_argument('--model_for_init', type=str, required=True, help='Model parameter to be used.')
    parser.add_argument('--model_for_reflection', type=str, required=True, help='Model parameter to be used.')
    parser.add_argument('--model_for_refinement', type=str, required=True, help='Model parameter to be used.')
    parser.add_argument('--add_gpt4_on_round', type=int, required=True, help='On which round to add GPT-4 to the method.')
    parser.add_argument('--max_iterations', type=int, required=True, help='Maximum number of iterations to refine the function.')
    parser.add_argument('--benchmark_type', type=str, required=True, help='"all" or "50"')
    parser.add_argument('--chunk_size', type=int, required=True, help='Number of items to process at a time to handle rate limits.')
    parser.add_argument('--delay_seconds', type=int, required=True, help='Delay in seconds between processing chunks to handle rate limits.')
    parser.add_argument('--tests_path', type=str, required=True, help='Which tests to use for the reflection process.')
    args = parser.parse_args()

    asyncio.run(main(args.model_for_init, args.model_for_reflection, args.model_for_refinement, args.add_gpt4_on_round, args.max_iterations, args.benchmark_type, args.chunk_size, args.delay_seconds, args.tests_path))
