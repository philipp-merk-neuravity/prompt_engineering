from utils.storage import load_benchmark

def extract_test_cases(obj):
    # Extract the test cases string from the object
    test_cases_str = obj["test"]
    
    # Initialize a list to store the formatted test cases
    test_cases_list = []
    
    # Split the test cases string into lines
    lines = test_cases_str.split('\n')
    
    # Iterate through each line
    for line in lines:
        # Check if the line contains an assert statement
        if 'assert' in line:
            # Remove leading and trailing spaces
            line = line.strip()
            # Add the line to the list
            test_cases_list.append(line)
    
    # remove tests that contain the str "assert True"
    test_cases_list = [test for test in test_cases_list if "assert True" not in test]
    return test_cases_list

benchmark_data = load_benchmark()
test_cases = []
for item in benchmark_data:
    current_test_cases = extract_test_cases(item)
    test_cases.append({
        "task_id": item["task_id"],
        "test_cases": current_test_cases
    })

# write to path: /home/neuravity/dev/prompt_engineering/test.jsonl
    
import json
with open('/home/neuravity/dev/prompt_engineering/test.jsonl', 'w') as file:
    for item in test_cases:
        file.write(json.dumps(item) + '\n')