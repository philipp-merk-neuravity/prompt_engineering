import asyncio
import argparse
from utils.code_generation import gen_function, gen_preprocessed_prompt
from utils.storage import load_benchmark, save_benchmark_results
from typing import List

async def preprocess_prompts(chunk, prompt_type):
    tasks = [gen_preprocessed_prompt(item["prompt"], prompt_type) for item in chunk]
    return await asyncio.gather(*tasks)

async def process_chunk(chunk, model, prompt_type, preprocessed_prompts: List[str]=None, temperature: float=0.2):
    if preprocessed_prompts is not None:
        tasks = [gen_function(item["prompt"], model, prompt_type, preprocessed_prompts[idx]) for idx, item in enumerate(chunk)]
    else:
        tasks = [gen_function(item["prompt"], model, prompt_type, temperature=temperature) for item in chunk]
    return await asyncio.gather(*tasks)

async def main(model, prompt_type, benchmark_type, chunk_size, delay_seconds, temperature):
    benchmark_data = load_benchmark(benchmark_type)[:1]
    items_to_save = []

    for i in range(0, len(benchmark_data), chunk_size):
        print(f"Processing chunk {i} to {i+chunk_size}")
        chunk = benchmark_data[i:i+chunk_size]
        
        if prompt_type == "scot" or prompt_type == "synth_few_shot_split":
            preprocessed_data = await preprocess_prompts(chunk, prompt_type)
            preprocessed_prompts = [item[0] for item in preprocessed_data]
            results = await process_chunk(chunk, model, prompt_type, preprocessed_prompts)
            results = [(results[idx][0],
                     preprocessed_data[idx][1] + results[idx][1],
                     preprocessed_data[idx][2] + results[idx][2],
                     preprocessed_data[idx][3] + results[idx][3]) for idx, result in enumerate(results)]
        else:
            results = await process_chunk(chunk, model, prompt_type, temperature=temperature)
        
        for result, item in zip(results, chunk):
            items_to_save.append({
                "task_id": item["task_id"],
                "generated_code": result[0],
                "prompt_tokens": result[1],
                "completion_tokens": result[2],
                "duration": result[3]
            })
        print(f"Processed {len(items_to_save)} items")
        await asyncio.sleep(delay_seconds)

    save_benchmark_results(items_to_save, benchmark_type, "simple", prompt_type, model, temperature)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run async tasks with model parameter.')
    parser.add_argument('--model', type=str, required=True, help='Model parameter to be used.')
    parser.add_argument('--prompt_type', type=str, required=True, help='io, few_shot, synth_few_shot, scot, zero_shot_cot, agentCoder')
    parser.add_argument('--benchmark_type', type=str, required=True, help='"all" or "50"')
    parser.add_argument('--chunk_size', type=int, required=True, help='Number of items to process at a time to handle rate limits.')
    parser.add_argument('--delay_seconds', type=int, required=True, help='Delay in seconds between processing chunks to handle rate limits.')
    parser.add_argument('--temperature', type=float, required=False, default=0.2, help='Temperature parameter for code generation.')

    args = parser.parse_args()
    asyncio.run(main(args.model, args.prompt_type, args.benchmark_type, args.chunk_size, args.delay_seconds, args.temperature))
