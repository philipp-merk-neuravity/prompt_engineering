import json
import numpy as np
import multiprocessing
import re

path_for_samples = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/simple/0.6/io/gpt-4-0125-preview"
path_for_tests = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/test_cases/few_shot/gpt-3.5-turbo-0125/with_refinement/gpt-4-0125-preview/init/init.jsonl"
predefined_tests_path = "/home/neuravity/dev/prompt_engineering/src/human_eval/data/ExtractedTests.json"

with open(predefined_tests_path, "r") as f:
    predefined_tests = json.load(f)

with open(path_for_tests, "r") as f:
    tests = [json.loads(line) for line in f.readlines()]

def pass_at_k(n, c, k): 
    """ 
    :param n: total number of samples 
    :param c: number of correct samples 
    :param k: k in pass@$k$ 
    """ 
    if n - c < k: 
        return 1.0 
    return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))

def run_tests(sample_code, tests, queue):
    results = []  # To store result of each test
    try:
        namespace = {}
        exec(sample_code, namespace)
        for test in tests:
            try:
                exec(test, namespace)
                results.append(True)  # Test passed
            except Exception:
                results.append(False)  # Test failed
        queue.put(results)  # Pass the list of results instead of a single True/False
    except Exception:
        queue.put([False] * len(tests))  # If an exception occurs before tests execution

def execute_sample_tests(sample_code, tests, timeout=15):
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=run_tests, args=(sample_code, tests, queue))
    process.start()
    process.join(timeout)
    if process.is_alive():
        process.terminate()
        process.join()
        return False, 0  # Assuming no tests passed if it times out
    else:
        test_results = queue.get()
        is_solved = all(test_results)  # Check if all tests are solved
        solved_count = sum(test_results)  # Count of solved tests
        return is_solved, solved_count

results = {}

for i in range(10):
    print(f"Processing sample size: {i}")
    samples_path = f"{path_for_samples}/{i}/{i}.jsonl"
    with open(samples_path, "r") as f:
        samples = [json.loads(line) for line in f.readlines()]
    current_results = []
    for test in tests:
        for sample in samples:
            if sample["task_id"] == test["task_id"]:
                print(f"Processing sample: {sample['task_id']}")
                is_solved, solved_count = execute_sample_tests(sample["generated_code"], test["tests"])
                sample_result = {
                    "task_id": sample["task_id"],
                    "is_solved": is_solved,
                    "solved_count": solved_count,
                }
                current_results.append(sample_result)
    results[i] = current_results

best_samples_for_generated_tests = {}

for i in range(10):
    current_best_results = []
    current_results = []
    for ix in range(i+1):
        current_results += results[ix]
        current_results.extend(results[ix])
    for test in tests:
        # lets first get all results of current_results that have the same task_id as test["task_id"]
        task_id = test["task_id"]
        task_results = [result for result in current_results if result["task_id"] == task_id]

        best_result = None
        best_solved_count = 0

        for result in task_results:
            if best_result is None:
                best_result = result
                best_solved_count = result["solved_count"]
            elif result["is_solved"]:
                best_result = result
                break
            elif not best_result["is_solved"] and result["solved_count"] > best_solved_count:
                best_result = result
                best_solved_count = result["solved_count"]
        current_best_results.append(best_result)
    best_samples_for_generated_tests[i] = current_best_results

def get_first_function_name(generated_code):
    match = re.search(r'def\s+([a-zA-Z_][a-zA-Z_0-9]*)\(', generated_code)
    return match.group(1) if match else None

for i in range(10):
    current_best_results = best_samples_for_generated_tests[i]
    for test in predefined_tests:
        task_id = test["task_id"]
        for result in current_best_results:
            if result["task_id"] == task_id:
                function_name = get_first_function_name(result["generated_code"])
                for test in test["tests"]:
                    test["tests"] = test["tests"].replace("candidate", function_name)
                is_solved, solved_count = execute_sample_tests(result["generated_code"], [test["tests"]])
                result["is_solved_for_predefined_tests"] = is_solved
                result["solved_count_for_predefined_tests"] = solved_count

pass_at_k_per_sample_size = {}

for i in range(10):
    current_best_results = []
    for ix in range(i+1):
        current_best_results.extend(best_samples_for_generated_tests[ix])
    c = [result["is_solved_for_predefined_tests"] for result in current_best_results].count(True)
    n = len(current_best_results)
    k = i + 1
    accuracy = pass_at_k(n, c, k)
    pass_at_k_per_sample_size[i] = accuracy

print(pass_at_k_per_sample_size)

    
    