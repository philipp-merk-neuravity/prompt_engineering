import asyncio
import argparse
from utils.code_generation import gen_function, gen_reflection, gen_refined_function
from utils.storage import load_benchmark, save_result, create_file_for_reflection, load_from_jsonl, load_multiline_data_from_jsonl, load_from_json
from utils.test_execution import get_test_results_async
from utils.data_conversion import convert_unit_test_results_to_str, get_unresolved_tasks
from utils.test_execution import get_test_results_async
import asyncio
import time
import random

async def async_refine_code(item, model_for_reflection, model_for_refinement, prompt_for_reflection, prompt_for_refinement, max_iterations, test_cases, file_path_for_results, init_result, temp_for_reflection, temp_for_refinement):
    generated_code = init_result["generated_code"]
    prompt_tokens = init_result["prompt_tokens"]
    completion_tokens = init_result["completion_tokens"]
    duration = init_result["duration"]
    iteration = 0
    best_solution = generated_code
    best_test_coverage = 0
    update_reflection = False
    reflection_for_best_solution = ""
    iteration_for_best_solution = 0
    iteration_states = []
    test_results_as_str_for_best_solution = ""
    while iteration < max_iterations:
        test_results, is_solved = await get_test_results_async(generated_code, test_cases)
        test_results_as_str = convert_unit_test_results_to_str(test_results)
        if (len(test_results["passed_tests"]) > best_test_coverage) and iteration > 0:
            best_solution = generated_code
            best_test_coverage = len(test_results["passed_tests"])
            update_reflection = True
            test_results_as_str_for_best_solution = test_results_as_str
        else:
            iteration_for_best_solution += 1
        
        if iteration == 0:
            test_results_as_str_for_best_solution = test_results_as_str

        iteration_states.append({
            "generated_code": best_solution,
            "is_solved": is_solved,
            "iteration": iteration,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "duration": duration
        })
        if is_solved or iteration == max_iterations - 1:
            break
        if update_reflection or reflection_for_best_solution == "" or iteration_for_best_solution == 2:
            reflection_for_best_solution, prompt_tokens_for_refl, completion_tokens_for_refl, duration_for_refl  = await gen_reflection(best_solution, test_results_as_str_for_best_solution, model_for_reflection, prompt_for_reflection, temperature=temp_for_reflection)
            prompt_tokens += prompt_tokens_for_refl
            completion_tokens += completion_tokens_for_refl
            duration += duration_for_refl
            update_reflection = False
            iteration_for_best_solution = 0
        generated_code, prompt_tokens_for_refinement, completions_tokens_for_refinement, duration_for_refinement = await gen_refined_function(item["prompt"], best_solution, test_results_as_str_for_best_solution, reflection_for_best_solution, model_for_refinement, prompt_for_refinement, temperature=temp_for_refinement)
        prompt_tokens += prompt_tokens_for_refinement
        completion_tokens += completions_tokens_for_refinement
        duration += duration_for_refinement + duration_for_refl
        iteration += 1
        
    results_for_task = {
        "task_id": item["task_id"],
        "generated_code": best_solution,
        "is_solved": is_solved,
        "iterations": iteration,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "duration": duration,
        "iteration_states": iteration_states
    }
    save_result(results_for_task, file_path_for_results)
    print(f"Task {item['task_id']} is solved: {is_solved}")

def pick_random_test_cases(test_cases, task_id, max_cases=4):
    # Filter test cases for the given task_id
    filtered_cases = [test_case for test_cases_group in test_cases
                      for test_case in test_cases_group["tests"]
                      if test_cases_group["task_id"] == task_id]
    return filtered_cases
    # return random.sample(filtered_cases, min(len(filtered_cases), max_cases))

def get_init_result(init_results, task_id):
    for result in init_results:
        if result["task_id"] == task_id:
            return result
    return None
async def process_single_chunk(chunk, model_for_reflection, model_for_refinement, prompt_for_reflection, prompt_for_refinement, max_iterations, test_cases, file_path_for_results, init_results, temp_for_refinement, temp_for_reflection):
    tasks = [
        async_refine_code(
            item,
            model_for_reflection,
            model_for_refinement,
            prompt_for_reflection,
            prompt_for_refinement,
            max_iterations,
            pick_random_test_cases(test_cases, item["task_id"]),
            file_path_for_results,
            get_init_result(init_results, item["task_id"]),
            temp_for_refinement=temp_for_refinement,
            temp_for_reflection=temp_for_reflection
        ) for item in chunk
    ]
    print(f"Processing {len(tasks)} items")
    return await asyncio.gather(*tasks)

async def process_chunks(benchmark_data, model_for_reflection, model_for_refinement, prompt_for_reflection, prompt_for_refinement, max_iterations, tests_cases, chunk_size, file_path_for_results, init_results, temp_for_reflection, temp_for_refinement):
    chunks = [benchmark_data[i:i + chunk_size] for i in range(0, len(benchmark_data), chunk_size)]
    all_results = []
    for chunk in chunks:
        results = await process_single_chunk(chunk, model_for_reflection, model_for_refinement, prompt_for_reflection, prompt_for_refinement, max_iterations, tests_cases, file_path_for_results, init_results, temp_for_reflection=temp_for_reflection , temp_for_refinement=temp_for_refinement)
        all_results.extend(results)
    return all_results

async def main(model_for_reflection, model_for_refinement, prompt_for_reflection, prompt_for_refinement, max_iterations, benchmark_type, chunk_size, tests_path, file_path_for_init, temp_for_reflection, temp_for_refinement, test_type):
    tests_path = tests_path
    folder_path_config = [
        [prompt_for_reflection, prompt_for_refinement],
        [temp_for_reflection, temp_for_refinement],
        [model_for_reflection]
    ]
    file_name_config = [
        "use_best",
        test_type
    ]       
    file_path_for_results = create_file_for_reflection("/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/reflection", folder_path_config, file_name_config)
    init_results = load_from_jsonl(file_path_for_init)
    current_benchmark_results = load_from_jsonl(file_path_for_results)
    benchmark_data = load_benchmark(benchmark_type)
    unresolved_tasks = get_unresolved_tasks(benchmark_data, current_benchmark_results)
    # test_cases = load_from_jsonl(tests_path)
    test_cases = load_multiline_data_from_jsonl(tests_path)[0]

    start_time = time.time()  # Capture start time
    all_results = await process_chunks(unresolved_tasks, model_for_reflection, model_for_refinement, prompt_for_reflection, prompt_for_refinement, max_iterations, test_cases, chunk_size, file_path_for_results, init_results, temp_for_reflection=temp_for_reflection , temp_for_refinement=temp_for_refinement)
    
    # save_benchmark_results_for_reflection(all_results, benchmark_type, "reflection", file_name_config)
    print(f"Processed {len(all_results)} items")
    end_time = time.time()  # Capture end time
    duration = end_time - start_time  # Calculate duration
    print(f"Function execution took {duration} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run async tasks for code generation with iterative refinement.')
    parser.add_argument('--model_for_reflection', type=str, required=True, help='Model parameter for reflection.')
    parser.add_argument('--model_for_refinement', type=str, required=True, help='Model parameter for refinement.')
    parser.add_argument('--prompt_for_reflection', type=str, required=True, help='Prompt for reflection.')
    parser.add_argument('--prompt_for_refinement', type=str, required=True, help='Prompt for refinement.')
    parser.add_argument('--max_iterations', type=int, required=True, help='Maximum number of iterations for refinement.')
    parser.add_argument('--benchmark_type', type=str, required=True, help='"all" or "50" to specify the benchmark dataset.')
    parser.add_argument('--chunk_size', type=int, required=True, help='Number of items per chunk for parallel processing.')
    parser.add_argument('--tests_path', type=str, required=True, help='Path to test cases for evaluating generated code.')
    parser.add_argument('--file_path_for_init', type=str, required=True, help='File path for simple results.')
    parser.add_argument('--temp_for_reflection', type=float, required=True, help='Temperature for reflection.')
    parser.add_argument('--temp_for_refinement', type=float, required=True, help='Temperature for refinement.')
    parser.add_argument("--test_type", type=str, required=True, help="Type of test cases to use for evaluation.")

    args = parser.parse_args()

    asyncio.run(main(args.model_for_reflection, args.model_for_refinement, args.prompt_for_reflection, args.prompt_for_refinement, args.max_iterations, args.benchmark_type, args.chunk_size, args.tests_path, args.file_path_for_init, args.temp_for_reflection, args.temp_for_refinement, args.test_type))