import json
path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/test_cases/few_shot/gpt-3.5-turbo-0125/with_refinement/gpt-4-0125-preview/5/5.jsonl"

all_data = []

all_prompt_tokens = 0
all_completion_tokens = 0
all_prompt_tokens_filter = 0
all_completion_tokens_filter = 0

# read the jsonl file
with open(path, 'r') as file:
    data = file.readlines()
    all_data = [json.loads(line)
                for line in data]

for item in all_data:
    prompt_tokens = item["prompt_tokens"]
    completion_tokens = item["completion_tokens"]
    prompt_tokens_filter = item["prompt_tokens_filter"]
    completion_tokens_filter = item["completion_tokens_filter"]
    all_prompt_tokens += prompt_tokens
    all_completion_tokens += completion_tokens
    all_prompt_tokens_filter += prompt_tokens_filter
    all_completion_tokens_filter += completion_tokens_filter

combined_results = {
    "prompt_tokens": all_prompt_tokens,
    "completion_tokens": all_completion_tokens,
    "prompt_tokens_filter": all_prompt_tokens_filter,
    "completion_tokens_filter": all_completion_tokens_filter
}

save_path = "/home/neuravity/dev/prompt_engineering/src/test"

with open(f"{save_path}/test_results_stats.json", 'w') as file:
    file.write(json.dumps(combined_results, indent=4))