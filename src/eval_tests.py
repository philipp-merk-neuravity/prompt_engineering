from utils.storage import load_benchmark, load_data_from_jsonl
from utils.test_execution import  check_test_accuracy
import asyncio
import argparse

import json  # Import the json module

async def main(path_for_test_cases):
    benchmark_data = load_benchmark("all")
    test_cases = load_data_from_jsonl(path_for_test_cases)
    all_test_results = []
    for benchmark_item in benchmark_data:
        for test_item in test_cases:
            if benchmark_item["task_id"] == test_item["task_id"]:
                test_results, is_solved = check_test_accuracy(benchmark_item["prompt"] + benchmark_item["canonical_solution"], test_item["generated_tests"])
                all_test_results.append({"task_id": benchmark_item["task_id"], "is_solved": is_solved, "test_results": test_results})
    folder_path = path_for_test_cases.rsplit("/", 1)[0]
    with open(f"{folder_path}/test_results.json", "w") as f:
        json.dump(all_test_results, f, indent=4)
    number_of_solved_tasks = [result["is_solved"] for result in all_test_results].count(True)
    number_of_failed_tasks = [result["is_solved"] for result in all_test_results].count(False)
    accuracy = number_of_solved_tasks / len(all_test_results)
    with open(f"{folder_path}/test_results_stats.json", "w") as f:
        json.dump({"number_of_solved_tasks": number_of_solved_tasks, "number_of_failed_tasks": number_of_failed_tasks, "accuracy": accuracy}, f, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run async tasks with model parameter.')
    parser.add_argument('--path_for_test_cases', type=str, required=True, help='Path to the test cases.')

    args = parser.parse_args()

    asyncio.run(main(args.path_for_test_cases))
