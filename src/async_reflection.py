import asyncio
import argparse
from utils.code_generation import gen_function, gen_reflection, gen_refined_function
from utils.storage import load_benchmark, save_benchmark_results, load_test_cases
from utils.test_execution import get_test_results
from typing import List

async def async_refine_code(item, model_for_init, model_for_reflection, model_for_refinement, max_iterations, tests_path):
    generated_code = await gen_function(item["prompt"], model_for_init)
    test_results, is_solved = await get_test_results(generated_code, tests_path)

    for iteration in range(max_iterations):
        if is_solved or iteration == max_iterations - 1:
            break
        reflection = await gen_reflection(generated_code, test_results, model_for_reflection)
        generated_code = await gen_refined_function(item["prompt"], generated_code, test_results, reflection, model_for_refinement)
        test_results, is_solved = await get_test_results(generated_code, tests_path)
        iteration += 1
    
    return {
        "task_id": item["task_id"],
        "generated_code": generated_code,
        "is_solved": is_solved
    }

async def process_single_chunk(chunk, model_for_init, model_for_reflection, model_for_refinement, max_iterations, tests_cases):
    tasks = [async_refine_code(item, model_for_init, model_for_reflection, model_for_refinement, max_iterations, tests_path) for item in chunk]
    return await asyncio.gather(*tasks)

async def process_chunks(benchmark_data, model_for_init, model_for_reflection, model_for_refinement, max_iterations, tests_cases, chunk_size):
    chunks = [benchmark_data[i:i + chunk_size] for i in range(0, len(benchmark_data), chunk_size)]
    tasks = [process_single_chunk(chunk, model_for_init, model_for_reflection, model_for_refinement, max_iterations, tests_cases) for chunk in chunks]
    results = await asyncio.gather(*tasks)
    return [item for sublist in results for item in sublist]

async def main(model_for_init, model_for_reflection, model_for_refinement, max_iterations, benchmark_type, chunk_size, delay_seconds, tests_path):
    benchmark_data = load_benchmark(benchmark_type)
    test_cases = load_test_cases()
    all_results = await process_chunks(benchmark_data, model_for_init, model_for_reflection, model_for_refinement, max_iterations, test_cases, chunk_size)
    
    # Save results
    for result in all_results:
        save_benchmark_results(result["task_id"], result["generated_code"], "Your desired format here")
    print(f"Processed {len(all_results)} items")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run async tasks for code generation with iterative refinement.')
    parser.add_argument('--model_for_init', type=str, required=True, help='Model parameter for initial code generation.')
    parser.add_argument('--model_for_reflection', type=str, required=True, help='Model parameter for reflection.')
    parser.add_argument('--model_for_refinement', type=str, required=True, help='Model parameter for refinement.')
    parser.add_argument('--max_iterations', type=int, required=True, help='Maximum number of iterations for refinement.')
    parser.add_argument('--benchmark_type', type=str, required=True, help='"all" or "50" to specify the benchmark dataset.')
    parser.add_argument('--chunk_size', type=int, required=True, help='Number of items per chunk for parallel processing.')
    parser.add_argument('--delay_seconds', type=int, required=True, help='Delay between processing chunks to manage rate limits.')
    parser.add_argument('--tests_path', type=str, required=True, help='Path to test cases for evaluating generated code.')

    args = parser.parse_args()

    asyncio.run(main(args.model_for_init, args.model_for_reflection, args.model_for_refinement, args.max_iterations, args.benchmark_type, args.chunk_size, args.delay_seconds, args.tests_path))
