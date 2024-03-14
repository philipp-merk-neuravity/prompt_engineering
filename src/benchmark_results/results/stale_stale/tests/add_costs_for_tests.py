import json

# File paths
file_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_tests/test_results.jsonl"
file_path_for_costs = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/costs.json"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_tests"

# Load .jsonl data
with open(file_path, 'r') as file:
    all_data = [json.loads(line) for line in file]

# Load .json data
with open(file_path_for_costs, 'r') as file:
    costs = json.load(file)

def calculate_cost(data, costs):
    overall_costs = []
    
    for item in data:
        model = item["model"]
        refinement_model = item.get("refinement_model")
        data_info = item["data"]
        
        prompt_tokens = data_info["prompt_tokens"]
        completion_tokens = data_info["completion_tokens"]
        
        # Determine tokens for calculation based on condition
        if refinement_model and model == "gpt-3.5-turbo-0125" and refinement_model == "gpt-4-0125-preview":
            prompt_tokens_filter = data_info["prompt_tokens_filter"]
            completion_tokens_filter = data_info["completion_tokens_filter"]
            # Costs calculation for both models
            cost_model = (prompt_tokens * costs[model]["input"] + completion_tokens * costs[model]["output"]) / 1000000
            cost_refinement_model = (prompt_tokens_filter * costs[refinement_model]["input"] + completion_tokens_filter * costs[refinement_model]["output"]) / 1000000
            total_cost = cost_model + cost_refinement_model
        else:
            # General cost calculation
            total_cost = (prompt_tokens * costs[model]["input"] + completion_tokens * costs[model]["output"]) / 1000000
        
        overall_costs.append({"model": model, "refinement_model": refinement_model, "type": item["type"], "total_cost": total_cost, "accuracy": item["accuracy"]})
    
    return overall_costs

overall_costs = calculate_cost(all_data, costs)

# save the costs
with open(save_path + "test_results_with_costs.json", 'w') as file:
    json.dump(overall_costs, file, indent=4)