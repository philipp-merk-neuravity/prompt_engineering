# import json

# # Function to apply min-max normalization
# def minmax_normalize(value, min_value, max_value):
#     return (value - min_value) / (max_value - min_value)

# def run_utility_analysis(accuracy, cost):
#     return accuracy ^ 0.8 
#     return accuracy * 0.8 - cost * 0.2

# # Load the test results
# path_for_tests = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_tests/test_results_with_costs.json"
# with open(path_for_tests, 'r') as file:
#     test_results = json.load(file)

# # Find the minimum and maximum values for accuracy and total_cost
# min_accuracy = min(test_results, key=lambda x: x['accuracy'])['accuracy']
# max_accuracy = max(test_results, key=lambda x: x['accuracy'])['accuracy']
# min_cost = min(test_results, key=lambda x: x['total_cost'])['total_cost']
# max_cost = max(test_results, key=lambda x: x['total_cost'])['total_cost']

# # Normalize the accuracy and total_cost, and calculate the utility score for each item
# for result in test_results:
#     result['normalized_accuracy'] = minmax_normalize(result['accuracy'], min_accuracy, max_accuracy)
#     result['normalized_total_cost'] = minmax_normalize(result['total_cost'], min_cost, max_cost)
#     # Calculate utility score using normalized values
#     result['utility_score'] = run_utility_analysis(result['normalized_accuracy'], result['normalized_total_cost'])

# # Save the updated test results with normalized costs and utility scores
# save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_tests/test_results_with_normalized_costs_and_utility.json"
# with open(save_path, 'w') as file:
#     json.dump(test_results, file, indent=4)

import json

# New utility function with non-linear relationship
def run_utility_analysis(accuracy, cost, a, c):
    if cost == 0:
        return accuracy
    return (accuracy ** a) / (cost ** c)

# Load the test results
path_for_tests = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_tests/test_results_with_costs.json"
with open(path_for_tests, 'r') as file:
    test_results = json.load(file)

# Find the minimum and maximum values for accuracy and total_cost for normalization purposes
min_accuracy = min(test_results, key=lambda x: x['accuracy'])['accuracy']
max_accuracy = max(test_results, key=lambda x: x['accuracy'])['accuracy']
min_cost = min(test_results, key=lambda x: x['total_cost'])['total_cost']
max_cost = max(test_results, key=lambda x: x['total_cost'])['total_cost']

# Parameters for non-linear utility function
a = 1.5  # Adjust as needed to prioritize accuracy
c = 1  # Adjust as needed to prioritize cost

# Normalize the accuracy and total_cost, and calculate the utility score for each item
for result in test_results:
    normalized_accuracy = (result['accuracy'] - min_accuracy) / (max_accuracy - min_accuracy)
    normalized_cost = (result['total_cost'] - min_cost) / (max_cost - min_cost)
    # Calculate utility score using non-linear utility function
    result['utility_score'] = run_utility_analysis(normalized_accuracy, normalized_cost, a, c)

# Save the updated test results with normalized costs and utility scores
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_tests/test_results_with_normalized_costs_and_utility.json"
with open(save_path, 'w') as file:
    json.dump(test_results, file, indent=4)
