import asyncio
import argparse
from utils.code_generation import gen_tests
from utils.storage import load_benchmark, save_generated_tests

async def process_chunk(chunk, model, prompt_type):
    tasks = [gen_tests(item["prompt"], model, prompt_type, 12) for item in chunk]
    return await asyncio.gather(*tasks)

async def main(model, prompt_type, chunk_size):
    benchmark_data = load_benchmark("all")
    items_to_save = []

    for i in range(0, len(benchmark_data), chunk_size):
        print(f"Processing chunk {i} to {i+chunk_size}")
        chunk = benchmark_data[i:i+chunk_size]
        results = await process_chunk(chunk, model, prompt_type)

        for result, item in zip(results, chunk):
            items_to_save.append({
                "task_id": item["task_id"],
                "generated_tests": result[0],
                "prompt_tokens": result[1],
                "completion_tokens": result[2],
                "duration": result[3]
            })
        print(f"Processed {len(items_to_save)} items")

    save_generated_tests(items_to_save, prompt_type, model)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run async tasks with model parameter.')
    parser.add_argument('--model', type=str, required=True, help='Model parameter to be used.')
    parser.add_argument('--prompt_type', type=str, required=True, help='io, few_shot, agentCoder')
    parser.add_argument('--chunk_size', type=int, required=True, help='Number of items to process at a time to handle rate limits.')

    args = parser.parse_args()

    asyncio.run(main(args.model, args.prompt_type, args.chunk_size))
