import json

def is_dominated(candidate, others):
    for other in others:
        if (other['accuracy'] > candidate['accuracy'] and other['total_cost'] < candidate['total_cost']):
            return True
    return False

def find_pareto_frontier(test_results):
    # First, mark all as not Pareto valuable
    for result in test_results:
        result['is_valuable_by_pareto'] = False
    
    # Find and mark Pareto frontier as valuable
    for candidate in test_results:
        if not is_dominated(candidate, test_results):
            candidate['is_valuable_by_pareto'] = True

# Load the test results from file
tests_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_tests/test_results_with_costs.json"
with open(tests_path, 'r') as file:
    data = json.load(file)

# Apply the Pareto principle to mark the valuable models
find_pareto_frontier(data)

# Save the entire data list with the 'is_valuable_by_pareto' status for all models
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_tests"
with open(save_path + "/test_results_with_pareto_status.json", 'w') as file:
    json.dump(data, file, indent=4)