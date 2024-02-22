from utils.storage import load_benchmark_results

file_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/50/simple/io/gpt-3.5-turbo"

for i in range(7):
    current_path = f"{file_path}/{i}/{i}.jsonl"
    results = load_benchmark_results(current_path)
    sum_completion_tokens = 0
    sum_prompt_tokens = 0
    sum_duration = 0

    for item in results:
        sum_duration += item["duration"]
        sum_completion_tokens += item["completion_tokens"]
        sum_prompt_tokens += item["prompt_tokens"]

    
    gpt_4_cost = sum_completion_tokens / 1000 * 0.0015 + sum_prompt_tokens / 1000 * 0.0005
    print(f"Tokens total: {sum_completion_tokens + sum_prompt_tokens}")
    print(f"Total cost for {i} is {gpt_4_cost} and total duration is {sum_duration} seconds.")
