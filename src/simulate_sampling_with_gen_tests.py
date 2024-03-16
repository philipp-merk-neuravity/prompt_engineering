# folder path for samples
# generated tests
# for i in range(10) -> execute generated tests for the corresponding sample size -> save the best result
# for round save the file with the best result
import json
path_for_samples = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/simple/0.6/io/gpt-4-0125-preview"
path_for_tests = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/test_cases/few_shot/gpt-3.5-turbo-0125/with_refinement/gpt-4-0125-preview/init/init.jsonl"

with open(path_for_tests, "r") as f:
    tests = [json.loads(line) for line in f.readlines()]

def execute_test(test, samples):
    # use exec() and namespace to execute the test
    most_tests_solved = 0
    best_result = None
    for sample in samples:
        current_most_tests_solved = 0
        for test_case in test["tests"]:
            # run the test
            # if the test is solved -> increment current_most_tests_solved
        # if current_most_tests_solved > most_tests_solved -> best_result = current_most_tests_solved and most_tests_solved = current_most_tests_solved
        if current_most_tests_solved > most_tests_solved:
            best_result = sample
            most_tests_solved = current_most_tests_solved
            
for i in range(10):
    all_samples_for_i = []
    for ix in range(10):
        current_sample_path = f"{path_for_samples}/{ix}/{ix}.jsonl"
        with open(current_sample_path, "r") as f:
            # read the jsonl appropriately
            samples = [json.loads(line) for line in f.readlines()]
            all_samples_for_i.append(samples)
    for test in tests:
        current_samples = [sample for sample in all_samples_for_i if sample["task_id"] == test["task_id"]]

