from utils.storage import load_benchmark_results
import json
import random
import os
from dotenv import load_dotenv

load_dotenv()
DEV_PATH = os.getenv('DEV_PATH')


path = f"{DEV_PATH}/src/benchmark_results/test_cases/few_shot/gpt-3.5-turbo-0125/without_refinement"

combined_results = []
randomly_selected_results = []

for i in range(5):
    current_path = path + f"/{i}/{i}.jsonl"
    print(current_path)
    combined_results.extend(load_benchmark_results(current_path))

iteration_file_path = path + "/0/0.jsonl"
iteration_file = load_benchmark_results(iteration_file_path)

for item in iteration_file:
    # lets get all items from combined_results that have the same item["task_id"] value
    task_id = item["task_id"]
    matching_items = [result for result in combined_results if result["task_id"] == task_id]
    # get 1 item from matching_items randomly using the library random
    random_item = random.choice(matching_items)
    randomly_selected_results.append(random_item)

with open(f"{path}/combined_results.jsonl", 'w') as file:
    for result in randomly_selected_results:
        file.write(json.dumps(result) + '\n')