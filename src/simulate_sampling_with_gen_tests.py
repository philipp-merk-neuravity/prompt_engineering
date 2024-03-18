import json
import numpy as np
import multiprocessing
import re
import subprocess

# Paths
method = "io"
model = "gpt-3.5-turbo-0125"
temperature = "0.8"
test_type = "tests_3.5_3.5"
save_path = f"/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/simpe_check_tests/{temperature}/{method}/{model}/{test_type}"
path_for_samples = f"/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/simple/{temperature}/{method}/{model}"
path_for_tests = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/test_cases/0.2/io/gpt-3.5-turbo-0125/with_refinement/gpt-3.5-turbo-0125/1/1.jsonl"
predefined_tests_path = "/home/neuravity/dev/prompt_engineering/src/human_eval/data/ExtractedTests.json"
evaluation_path = "/home/neuravity/dev/prompt_engineering/src/human_eval/human_eval/evaluate_functional_correctness.py"
script_path = "/home/neuravity/dev/prompt_engineering/src/human_eval/human_eval/evaluate_functional_correctness.py"
problem_file_path = "/home/neuravity/dev/prompt_engineering/src/human_eval/data/HumanEval.jsonl"
max_sample_size = 10

# Load predefined tests
with open(predefined_tests_path, "r") as f:
    predefined_tests = json.load(f)

# Load tests
with open(path_for_tests, "r") as f:
    tests = [json.loads(line) for line in f.readlines()]

# Function to run tests and capture results
def run_tests(sample_code, tests, queue):
    results = []
    try:
        namespace = {}
        exec(sample_code, namespace)
        for test in tests:
            try:
                exec(test, namespace)
                results.append(True)
            except Exception:
                results.append(False)
        queue.put(results)
    except Exception:
        queue.put([False] * len(tests))

# Function to execute sample tests with timeout
def execute_sample_tests(sample_code, tests, timeout=6):
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=run_tests, args=(sample_code, tests, queue))
    process.start()
    process.join(timeout)
    if process.is_alive():
        process.terminate()
        process.join()
        return False, 0
    else:
        test_results = queue.get()
        is_solved = all(test_results)
        solved_count = sum(test_results)
        return is_solved, solved_count

# Function to process sample tests
def process_samples():
    results = {}
    for i in range(max_sample_size):
        samples_path = f"{path_for_samples}/{i}/{i}.jsonl"
        with open(samples_path, "r") as f:
            samples = [json.loads(line) for line in f.readlines()]
        current_results = []
        for test in tests:
            for sample in samples:
                if sample["task_id"] == test["task_id"]:
                    is_solved, solved_count = execute_sample_tests(sample["generated_code"], test["tests"])
                    sample_result = {
                        "task_id": sample["task_id"],
                        "is_solved": is_solved,
                        "solved_count": solved_count,
                        "generated_code": sample["generated_code"],
                        "prompt_tokens": sample["prompt_tokens"],
                        "completion_tokens": sample["completion_tokens"],
                        "duration": sample["duration"],
                    }
                    current_results.append(sample_result)
        results[i] = current_results
    return results

# Function to find best samples
def find_best_samples(results):
    best_samples_for_generated_tests = {}
    for i in range(max_sample_size):
        current_best_results = []
        current_results = []
        for ix in range(max_sample_size):
            random_numbers = np.random.choice(max_sample_size, i+1, replace=False)
            for random_number in random_numbers:
                current_results += results[random_number]
            for test in tests:
                task_id = test["task_id"]
                task_results = [result for result in current_results if result["task_id"] == task_id]

                best_result = None
                is_solved = False
                best_solved_count = 0

                for result in task_results:
                    if best_result is None or (not is_solved and result["solved_count"] > best_solved_count):
                        best_result = result
                        best_solved_count = result["solved_count"]
                        is_solved = result["is_solved"]
                current_best_results.append(best_result)
            best_samples_for_generated_tests[i] = current_best_results
    print("Found best samples for generated tests")
    return best_samples_for_generated_tests

# Function to get the first function name from code
def get_first_function_name(generated_code):
    match = re.search(r'def\s+([a-zA-Z_][a-zA-Z_0-9]*)\(', generated_code)
    return match.group(1) if match else None

# Function to execute predefined tests
def execute_predefined_tests(best_samples_for_generated_tests):
    for i in range(max_sample_size):
        current_best_results = best_samples_for_generated_tests[i]
        for test in predefined_tests:
            task_id = test["task_id"]
            for result in current_best_results:
                if result["task_id"] == task_id:
                    function_name = get_first_function_name(result["generated_code"])
                    modified_tests = [current_test.replace("candidate", function_name) for current_test in test["tests"]]
                    is_solved, solved_count = execute_sample_tests(result["generated_code"], modified_tests)
                    result["is_solved_for_predefined_tests"] = is_solved
                    result["solved_count_for_predefined_tests"] = solved_count
    print("Executed predefined tests")
    return best_samples_for_generated_tests

# Function to calculate pass@k per sample size
def calculate_pass_at_k_per_sample_size(best_samples_for_generated_tests):
    command = [
        "python", script_path,
        "--sample_file", best_samples_for_generated_tests,
        "--problem_file", problem_file_path,
        "--k", "1",
    ]
    subprocess.run(command)

# Main execution flow
def main():
    results_per_sample_size = process_samples()
    best_samples = find_best_samples(results_per_sample_size)
    for i in range(max_sample_size):
        # first create the folders 0-9
        subprocess.run(["mkdir", f"{save_path}/{i}"])
        with open(f"{save_path}/{i}/combined_results.jsonl", "w") as f:
            for result in best_samples[i]:
                f.write(json.dumps(result) + "\n")

    for i in range(max_sample_size):
        current_results_path = f"{save_path}/{i}/combined_results.jsonl"
        calculate_pass_at_k_per_sample_size(current_results_path)
if __name__ == "__main__":
    main()
