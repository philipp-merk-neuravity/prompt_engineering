from utils.storage import load_benchmark, load_from_json, load_test_cases
from utils.test_execution import  check_test_accuracy, get_test_results_async, get_test_results_2
import asyncio
import argparse
import json  



# async def main(path_for_test_cases):
#     benchmark_data = load_benchmark("all")
#     test_cases = load_test_cases(path_for_test_cases)
#     all_test_results = []
#     for benchmark_item in benchmark_data:
#         for test_item in test_cases:
#             if benchmark_item["task_id"] == test_item["task_id"]:
#                 print(f"Running tests for task {benchmark_item['task_id']}")
#                 test_results, is_solved = await get_test_results_2(benchmark_item["prompt"] + benchmark_item["canonical_solution"], test_item["generated_tests"])
#                 all_test_results.append({"task_id": benchmark_item["task_id"], "is_solved": is_solved, "test_results": test_results})
#     folder_path = path_for_test_cases.rsplit("/", 1)[0]
#     with open(f"{folder_path}/test_results.json", "w") as f:
#         json.dump(all_test_results, f, indent=4)
#     number_of_solved_tasks = [result["is_solved"] for result in all_test_results].count(True)
#     number_of_failed_tasks = [result["is_solved"] for result in all_test_results].count(False)
#     accuracy = number_of_solved_tasks / len(all_test_results)
#     with open(f"{folder_path}/test_results_stats.json", "w") as f:
#         json.dump({"number_of_solved_tasks": number_of_solved_tasks, "number_of_failed_tasks": number_of_failed_tasks, "accuracy": accuracy}, f, indent=4)

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Run async tasks with model parameter.')
#     parser.add_argument('--path_for_test_cases', type=str, required=True, help='Path to the test cases.')

#     args = parser.parse_args()

#     asyncio.run(main(args.path_for_test_cases))


from utils.storage import load_benchmark
from utils.test_execution import  check_test_accuracy, get_test_results_2
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import argparse
import json
import asyncio

def load_multiline_data_from_jsonl(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            # Wrap the file content in square brackets and replace the last comma with an empty space if needed
            json_content = "[" + file_content.rstrip(',') + "]"
            data = json.loads(json_content)
            return data
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file at {file_path}: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

async def run_test_case_in_executor(executor, code_solution, test_cases):
    loop = asyncio.get_running_loop()
    # Use run_in_executor to run blocking functions in the process pool
    test_results, is_solved = await loop.run_in_executor(executor, check_test_accuracy, code_solution, test_cases)
    return test_results, is_solved

async def main(path_for_test_cases):
    benchmark_data = load_benchmark("all")[:1]
    # test_cases = (path_for_test_cases)
    test_cases = load_test_cases(path_for_test_cases)
    all_test_results = []

    # Create a ProcessPoolExecutor; the number of workers can be adjusted
    executor = ProcessPoolExecutor(max_workers=multiprocessing.cpu_count())

    tasks = []
    for benchmark_item in benchmark_data:
        for test_item in test_cases:
            if benchmark_item["task_id"] == test_item["task_id"]:
                code_solution = benchmark_item["prompt"] + benchmark_item["canonical_solution"]
                task = run_test_case_in_executor(executor, code_solution, test_item["tests"])
                tasks.append(task)

    results = await asyncio.gather(*tasks)

    for result, (benchmark_item, test_item) in zip(results, [(benchmark_item, test_item) for benchmark_item in benchmark_data for test_item in test_cases if benchmark_item["task_id"] == test_item["task_id"]]):
        test_results, is_solved = result
        all_test_results.append({"task_id": benchmark_item["task_id"], "is_solved": is_solved, "test_results": test_results})

    # Process results and write to files
    folder_path = path_for_test_cases.rsplit("/", 1)[0]
    with open(f"{folder_path}/test_results.json", "w") as f:
        json.dump(all_test_results, f, indent=4)

    number_of_solved_tasks = sum(result["is_solved"] for result in all_test_results)
    number_of_failed_tasks = len(all_test_results) - number_of_solved_tasks
    accuracy = number_of_solved_tasks / len(all_test_results) if all_test_results else 0

    with open(f"{folder_path}/test_results_stats.json", "w") as f:
        json.dump({
            "number_of_solved_tasks": number_of_solved_tasks,
            "number_of_failed_tasks": number_of_failed_tasks,
            "accuracy": accuracy
        }, f, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run async tasks with model parameter.')
    parser.add_argument('--path_for_test_cases', type=str, required=True, help='Path to the test cases.')

    args = parser.parse_args()

    asyncio.run(main(args.path_for_test_cases))
