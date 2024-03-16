import numpy as np
import json

path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/test_cases/0.4/few_shot/gpt-3.5-turbo-0125/without_refinement"

def estimator(n: int, c: int, k: int) -> float:
    """ 
    :param n: total number of samples 
    :param c: number of correct samples 
    :param k: k in pass@$k$ 
    """ 
    if n - c < k:
        return 1.0
    return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))

all_results = []

for i in range(0, 5):
    with open(f"{path}/{i}/test_results.json") as f:
        # load all data first
        data = json.load(f)
    for result in data:
        all_results.append(result)

n = len(all_results)
c = sum([result["is_solved"] for result in all_results])
k = 1

pass_at_k = estimator(n, c, k)

# save the number
with open(f"{path}/pass_at_{k}.json", "w") as f:
    f.write(json.dumps(pass_at_k))
