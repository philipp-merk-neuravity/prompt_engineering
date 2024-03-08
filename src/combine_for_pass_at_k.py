from utils.storage import load_from_jsonl

paths =  [
    "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/simple/io/gpt-3.5-turbo-0125-temp-0_68/12/12.jsonl_results.jsonl",
    "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/simple/io/gpt-3.5-turbo-0125-temp-0_68/13/13.jsonl_results.jsonl",
    "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/simple/io/gpt-3.5-turbo-0125-temp-0_68/14/14.jsonl_results.jsonl",
    "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/simple/io/gpt-3.5-turbo-0125-temp-0_68/15/15.jsonl_results.jsonl",
    "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/simple/io/gpt-3.5-turbo-0125-temp-0_68/16/16.jsonl_results.jsonl"
    ]


path_0 = paths[0]
data_0 = load_from_jsonl(path_0)

pass_for_all = []

for i, item in enumerate(data_0):
    current_is_solved = False
    for i in range(1, len(paths)):
        path = paths[i]
        data_n = load_from_jsonl(path)
        for current_item in data_n:
            if item["task_id"] == current_item["task_id"] and current_item["passed"]:
                current_is_solved = True
                break
    pass_for_all.append({
        "task_id": item["task_id"],
        "passed": current_is_solved
    })

is_solved_count = 0
for item in pass_for_all:
    if item["passed"]:
        is_solved_count += 1

print(is_solved_count/len(pass_for_all))
print("hi")