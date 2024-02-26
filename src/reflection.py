import asyncio
import argparse
from utils.code_generation import gen_function, gen_reflection, gen_refined_function
from utils.storage import load_benchmark, load_from_json, save_result, create_file_for_reflection, load_data_from_jsonl
from utils.test_execution import get_test_results_async
from utils.data_conversion import convert_unit_test_results_to_str, get_unresolved_tasks
from utils.test_execution import get_test_results_async
import asyncio
import time

async def async_refine_code(item, model_for_init, model_for_reflection, model_for_refinement, prompt_for_reflection, prompt_for_refinement, max_iterations, test_cases, file_path_for_results):
    generated_code, prompt_tokens, completions_tokens, duration  = await gen_function(item["prompt"], model_for_init)
    iteration = 0
    while iteration < max_iterations:
        test_results, is_solved = await get_test_results_async(generated_code, test_cases)
        test_results_as_str = convert_unit_test_results_to_str(test_results)
        if is_solved or iteration == max_iterations - 1:
            break
        reflection, prompt_tokens_for_refl, completion_tokens_for_refl, duration_for_refl  = await gen_reflection(generated_code, test_results_as_str, model_for_reflection, prompt_for_reflection)
        generated_code, prompt_tokens_for_refinement, completions_tokens_for_refinement, duration_for_refinement = await gen_refined_function(item["prompt"], generated_code, test_results_as_str, reflection, model_for_refinement, prompt_for_refinement)
        prompt_tokens += prompt_tokens_for_refinement + prompt_tokens_for_refl
        completions_tokens += completions_tokens_for_refinement + completion_tokens_for_refl
        duration += duration_for_refinement + duration_for_refl
        iteration += 1
        
    results_for_task = {
        "task_id": item["task_id"],
        "generated_code": generated_code,
        "is_solved": is_solved,
        "iterations": iteration,
        "prompt_tokens": prompt_tokens,
        "completions_tokens": completions_tokens,
        "duration": duration
    }
    save_result(results_for_task, file_path_for_results)
    print(f"Task {item['task_id']} is solved: {is_solved}")

async def process_single_chunk(chunk, model_for_init, model_for_reflection, model_for_refinement, prompt_for_reflection, prompt_for_refinement, max_iterations, test_cases, file_path_for_results):
    tasks = [
    async_refine_code(
        item,
        model_for_init,
        model_for_reflection,
        model_for_refinement,
        prompt_for_reflection,
        prompt_for_refinement,
        max_iterations,
        [test_case for test_cases in test_cases for test_case in test_cases["tests"] if test_cases["task_id"] == item["task_id"]],
        file_path_for_results
    ) 
    for item in chunk
    ]
    print(f"Processing {len(tasks)} items")
    return await asyncio.gather(*tasks)

async def process_chunks(benchmark_data, model_for_init, model_for_reflection, model_for_refinement, prompt_for_reflection, prompt_for_refinement, max_iterations, tests_cases, chunk_size, file_path_for_results):
    chunks = [benchmark_data[i:i + chunk_size] for i in range(0, len(benchmark_data), chunk_size)]
    all_results = []
    for chunk in chunks:
        results = await process_single_chunk(chunk, model_for_init, model_for_reflection, model_for_refinement, prompt_for_reflection, prompt_for_refinement, max_iterations, tests_cases, file_path_for_results)
        all_results.extend(results)
    return all_results

async def main(model_for_init, model_for_reflection, model_for_refinement, prompt_for_reflection, prompt_for_refinement, max_iterations, benchmark_type, chunk_size, tests_path):
    tests_path = tests_path
    file_name_config = {
        "use_gpt-4_at_round": None,
        "prompt_for_reflection": prompt_for_reflection,
        "prompt_for_refinement": prompt_for_refinement,
        "model_for_reflection": model_for_reflection,
        "model_for_refinement": model_for_refinement,
    }
    file_path_for_results = create_file_for_reflection(benchmark_type, "reflection", file_name_config)
    current_benchmark_results = load_data_from_jsonl(file_path_for_results)
    benchmark_data = load_benchmark(benchmark_type)
    unresolved_tasks = get_unresolved_tasks(benchmark_data, current_benchmark_results)
    test_cases = load_from_json(tests_path)

    start_time = time.time()  # Capture start time
    all_results = await process_chunks(unresolved_tasks, model_for_init, model_for_reflection, model_for_refinement, prompt_for_reflection, prompt_for_refinement, max_iterations, test_cases, chunk_size, file_path_for_results)
    
    # save_benchmark_results_for_reflection(all_results, benchmark_type, "reflection", file_name_config)
    print(f"Processed {len(all_results)} items")
    end_time = time.time()  # Capture end time
    duration = end_time - start_time  # Calculate duration
    print(f"Function execution took {duration} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run async tasks for code generation with iterative refinement.')
    parser.add_argument('--model_for_init', type=str, required=True, help='Model parameter for initial code generation.')
    parser.add_argument('--model_for_reflection', type=str, required=True, help='Model parameter for reflection.')
    parser.add_argument('--model_for_refinement', type=str, required=True, help='Model parameter for refinement.')
    parser.add_argument('--prompt_for_reflection', type=str, required=True, help='Prompt for reflection.')
    parser.add_argument('--prompt_for_refinement', type=str, required=True, help='Prompt for refinement.')
    parser.add_argument('--max_iterations', type=int, required=True, help='Maximum number of iterations for refinement.')
    parser.add_argument('--benchmark_type', type=str, required=True, help='"all" or "50" to specify the benchmark dataset.')
    parser.add_argument('--chunk_size', type=int, required=True, help='Number of items per chunk for parallel processing.')
    parser.add_argument('--tests_path', type=str, required=True, help='Path to test cases for evaluating generated code.')

    args = parser.parse_args()

    asyncio.run(main(args.model_for_init, args.model_for_reflection, args.model_for_refinement, args.prompt_for_reflection, args.prompt_for_refinement, args.max_iterations, args.benchmark_type, args.chunk_size, args.tests_path))