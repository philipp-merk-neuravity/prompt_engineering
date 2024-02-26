from src.utils.storage import load_benchmark_results
import json

path = "/home/neuravity/dev/prompt_engineering/src/human_eval/data/HumanEval.jsonl"

def extract_tests(task_json):
    # Extracting the test string from the given JSON
    test_str = task_json['test']
    
    # Removing unnecessary parts from the start until the first "assert"
    first_assert_index = test_str.find("assert")
    if first_assert_index != -1:
        trimmed_test_str = test_str[first_assert_index:]
    else:
        # If no "assert" found, return an empty list
        return []

    # Splitting the rest before each "assert", ensuring "assert" remains part of the statements
    split_asserts = trimmed_test_str.split("assert")
    # Re-adding "assert" to each split part except the first empty one due to the initial split
    assert_statements = ["assert" + assert_str for assert_str in split_asserts if assert_str]

    # Cleaning any leading or trailing whitespaces
    cleaned_asserts = [assert_statement.strip() for assert_statement in assert_statements]
    
    return cleaned_asserts

tests = []
result_data = load_benchmark_results(path)
for item in result_data:
    formatted_tests = extract_tests(item)
    formatted_item = {"task_id": item["task_id"], "tests": formatted_tests}
    tests.append(formatted_item)

# Specify the path where you want to save the JSON file
output_path = "/home/neuravity/dev/prompt_engineering/src/human_eval/data/ExtractedTests.json"

# Saving the tests list to a file in JSON format
with open(output_path, 'w') as outfile:
    json.dump(tests, outfile, indent=4)

print(f"Extracted tests saved to {output_path}")