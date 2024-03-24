import asyncio
import argparse
from utils.code_generation import gen_tests
from utils.storage import load_benchmark, save_generated_tests
import os
from dotenv import load_dotenv

load_dotenv()
# Fetch the environment variable 'DEV_PATH' defined in your system
DEV_PATH = os.getenv('DEV_PATH')


async def process_chunk(chunk, model, prompt_type, model_for_refinement, use_refinement, temperature):
    tasks = [gen_tests(item["prompt"], model, prompt_type, model_for_refinement=model_for_refinement, use_refinement=use_refinement, temperature=temperature, amount=10) for item in chunk]
    return await asyncio.gather(*tasks)
    
async def main(model, prompt_type, chunk_size, model_for_refinement, temperature):
    use_refinement = model_for_refinement != ""
    benchmark_data = load_benchmark("all")
    items_to_save = []

    for i in range(0, len(benchmark_data), chunk_size):
        print(f"Processing chunk {i} to {i+chunk_size}")
        chunk = benchmark_data[i:i+chunk_size]
        results = await process_chunk(chunk, model, prompt_type, model_for_refinement, use_refinement, temperature)
        
        for result, item in zip(results, chunk):
            items_to_save.append({
                "task_id": item["task_id"],
                "tests": result[0],
                "prompt_tokens": result[1],
                "completion_tokens": result[2],
                "duration": result[3],
                "prompt_tokens_filter": result[4] if use_refinement else 0,
                "completion_tokens_filter": result[5] if use_refinement else 0,
                "duration_filter": result[6] if use_refinement else 0
            })
        print(f"Processed {len(items_to_save)} items")

    save_generated_tests(items_to_save, prompt_type, model, model_for_refinement, use_refinement, temperature)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run async tasks with model parameter.')
    parser.add_argument('--model', type=str, required=True, help='Model parameter to be used.')
    parser.add_argument('--prompt_type', type=str, required=True, help='io, few_shot, agentCoder')
    parser.add_argument('--chunk_size', type=int, required=True, help='Number of items to process at a time to handle rate limits.')
    parser.add_argument('--model_for_refinement', type=str, required=False, help='Model parameter to be used for test refinement.')
    parser.add_argument('--temperature', type=float, required=True, help='Temperature parameter for generation.')

    args = parser.parse_args()

    asyncio.run(main(args.model, args.prompt_type, args.chunk_size, args.model_for_refinement, args.temperature))

# import asyncio
# import argparse
# from utils.code_generation import gen_tests
# from utils.storage import load_benchmark, save_generated_tests
# import json

# async def main(model, prompt_type):
#     benchmark_data = load_benchmark("all")[161:]

#     for benchmark_item in benchmark_data:
#         print(benchmark_item["task_id"])
#         generated_tests, tokens_for_prompt, tokens_for_completion, duration = await gen_tests(benchmark_item["prompt"], model, prompt_type, 12)
#         formatted_test_result = {
#                 "task_id": benchmark_item["task_id"],
#                 "generated_tests": generated_tests,
#                 "prompt_tokens": tokens_for_prompt,
#                 "completion_tokens": tokens_for_completion,
#                 "duration": duration
#         }
#         # write to: $DEV_PATH/src/benchmark_results/test_cases/few_shot/gpt-4/0/0.jsonl
#         with open(ff"{DEV_PATH}/src/benchmark_results/test_cases/few_shot/gpt-4/0/0.jsonl", "a") as f:
#             # use json.dump
#             json.dump(formatted_test_result, f, indent=4)

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Run async tasks with model parameter.')
#     parser.add_argument('--model', type=str, required=True, help='Model parameter to be used.')
#     parser.add_argument('--prompt_type', type=str, required=True, help='io, few_shot, agentCoder')

#     args = parser.parse_args()

#     asyncio.run(main(args.model, args.prompt_type))
