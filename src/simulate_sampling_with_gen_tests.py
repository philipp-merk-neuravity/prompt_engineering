import json
import numpy as np
import multiprocessing
import re
import subprocess
import os
import argparse
from dotenv import load_dotenv

load_dotenv()
# Fetch the environment variable 'DEV_PATH' defined in your system
DEV_PATH = os.getenv('DEV_PATH')




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
def process_samples(max_sample_size, path_for_samples, tests):
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

def find_best_samples(results, max_sample_size, tests):
    simulation_count = 20
    best_samples_for_generated_tests = {}
    for i in range(max_sample_size):
        current_best_results = []
        for ix in range(simulation_count):
            current_results = []
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

# Function to calculate pass@k per sample size
def calculate_pass_at_k_per_sample_size(best_samples_for_generated_tests, script_path, problem_file_path):
    command = [
        "python", script_path,
        "--sample_file", best_samples_for_generated_tests,
        "--problem_file", problem_file_path,
        "--k", "1",
    ]
    subprocess.run(command)

# Main execution flow
def main(method, model, temperature, test_type, test_path):
    save_path = f"{DEV_PATH}/src/benchmark_results/code_gen/simple_check_tests/{temperature}/{method}/{model}/{test_type}"
    path_for_samples = f"{DEV_PATH}/src/benchmark_results/code_gen/simple/{temperature}/{method}/{model}"
    path_for_tests = f"{DEV_PATH}/src/benchmark_results/test_cases/0.2/{test_path}"
    script_path = f"{DEV_PATH}/src/human_eval/human_eval/evaluate_functional_correctness.py"
    problem_file_path = f"{DEV_PATH}/src/human_eval/data/HumanEval.jsonl"
    max_sample_size = 10

    with open(path_for_tests, "r") as f:
        tests = [json.loads(line) for line in f.readlines()]

    results_per_sample_size = process_samples(
        max_sample_size,
        path_for_samples,
        tests
    )
    print(results_per_sample_size)

    best_samples = find_best_samples(
        results_per_sample_size,
        max_sample_size,
        tests
    )

    for i in range(max_sample_size):
        subprocess.run(["mkdir", f"{save_path}/{i}"])
        with open(f"{save_path}/{i}/combined_results.jsonl", "w") as f:
            for result in best_samples[i]:
                f.write(json.dumps(result) + "\n")

    for i in range(max_sample_size):
        current_results_path = f"{save_path}/{i}/combined_results.jsonl"
        calculate_pass_at_k_per_sample_size(
            current_results_path,
            script_path,
            problem_file_path
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run async tasks for code generation with iterative refinement.')
    parser.add_argument('--method', type=str, required=True, help='Model parameter for reflection.')
    parser.add_argument('--model', type=str, required=True, help='Model parameter for refinement.')
    parser.add_argument('--temperature', type=str, required=True, help='Model parameter for refinement.')
    parser.add_argument('--test_type', type=str, required=True, help='Model parameter for refinement.')
    parser.add_argument('--test_path', type=str, required=True, help='Model parameter for refinement.')

    args = parser.parse_args()

    main(
        method=args.method,
        model=args.model,
        temperature=args.temperature,
        test_type=args.test_type,
        test_path=args.test_path
    )

        