# import json
# import os

# base_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/simple/0.2"
# costs_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/costs.json"

# sub_folders = [
#     "io",
#     "scot",
#     "synth_few_shot_split",
#     "zero_shot_cot"
# ]

# models = [
#     "gpt-3.5-turbo-0125",
#     "gpt-4-0125-preview"
# ]

# output_for_gpt_3_5 = {
#     "Zero-Shot": [],
#     "SCoT": [],
#     "Synth. Few-Shots": [],
#     "Zero-Shot CoT": []
# }

# output_for_gpt_4 = {
#     "Zero-Shot": [],
#     "SCoT": [],
#     "Synth. Few-Shots": [],
#     "Zero-Shot CoT": []
# }

# file_name = "combined_results.jsonl_stats.json"

# with open(costs_path, "r") as file:
#     costs = json.load(file)

# for sub_folder in sub_folders:
#     sub_folder_path = f"{base_path}/{sub_folder}"
#     for model in models:
#         file_path = f"{sub_folder_path}/{model}/{file_name}"
#         with open(file_path, "r") as file:
#             line = file.readline()
#             result = json.loads(line)
#             input_costs_factor = costs[model]["input"]
#             output_costs_factor = costs[model]["output"]
#             input_costs = result["prompt_tokens"] * input_costs_factor / 1000000
#             output_costs = result["completion_tokens"] * output_costs_factor / 1000000
#             if model == "gpt-3.5-turbo-0125":
#                 combined_results_for_gpt3 = {
#                     sub_folder: {
#                         "accuracy": result["accuracy"],
#                         "prompt_tokens": result["prompt_tokens"],
#                         "completion_tokens": result["completion_tokens"],
#                         "duration": result["duration"],
#                         "cost": {
#                             "input": input_costs,
#                             "output": output_costs,
#                         }
#                     }
#                 }
#                 if sub_folder == "io":
#                     output_for_gpt_3_5["Zero-Shot"].append(combined_results_for_gpt3)
#                 elif sub_folder == "scot":
#                     output_for_gpt_3_5["SCoT"].append(combined_results_for_gpt3)
#                 elif sub_folder == "synth_few_shot_split":
#                     output_for_gpt_3_5["Synth. Few-Shots"].append(combined_results_for_gpt3)
#                 elif sub_folder == "zero_shot_cot":
#                     output_for_gpt_3_5["Zero-Shot CoT"].append(combined_results_for_gpt3)
#             elif model == "gpt-4-0125-preview":
#                 combined_results_for_gpt4 = {
#                     sub_folder: {
#                         "accuracy": result["accuracy"],
#                         "prompt_tokens": result["prompt_tokens"],
#                         "completion_tokens": result["completion_tokens"],
#                         "duration": result["duration"],
#                         "cost": {
#                             "input": input_costs,
#                             "output": output_costs,
#                         }
#                     }
#                 }
#                 if sub_folder == "io":
#                     output_for_gpt_4["Zero-Shot"].append(combined_results_for_gpt4)
#                 elif sub_folder == "scot":
#                     output_for_gpt_4["SCoT"].append(combined_results_for_gpt4)
#                 elif sub_folder == "synth_few_shot_split":
#                     output_for_gpt_4["Synth. Few-Shots"].append(combined_results_for_gpt4)
#                 elif sub_folder == "zero_shot_cot":
#                     output_for_gpt_4["Zero-Shot CoT"].append(combined_results_for_gpt4)

# save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_prompt_method/0.2"
# combined_results_for_gpt3_path = f"{save_path}/combined_results_for_gpt3.json"
# combined_results_for_gpt4_path = f"{save_path}/combined_results_for_gpt4.json"

# def save_results(file_path, data):
#     with open(file_path, 'w') as f:
#         for method, results in data.items():
#             for result in results:
#                 f.write(json.dumps(result) + '\n')

# save_results(combined_results_for_gpt3_path, output_for_gpt_3_5)
# save_results(combined_results_for_gpt4_path, output_for_gpt_4)

import json

base_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/simple/0.2"
costs_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/costs.json"

sub_folders = [
    "io",
    "scot",
    "synth_few_shot_split",
    "zero_shot_cot"
]

models = [
    "gpt-3.5-turbo-0125",
    "gpt-4-0125-preview"
]

output_for_gpt_3_5 = {
    "Zero-Shot": [],
    "SCoT": [],
    "Synth. Few-Shots": [],
    "Zero-Shot CoT": []
}

output_for_gpt_4 = {
    "Zero-Shot": [],
    "SCoT": [],
    "Synth. Few-Shots": [],
    "Zero-Shot CoT": []
}

file_name = "combined_results.jsonl_stats.json"

with open(costs_path, "r") as file:
    costs = json.load(file)

for sub_folder in sub_folders:
    sub_folder_path = f"{base_path}/{sub_folder}"
    for model in models:
        file_path = f"{sub_folder_path}/{model}/{file_name}"
        with open(file_path, "r") as file:
            line = file.readline()
            result = json.loads(line)
            input_costs_factor = costs[model]["input"]
            output_costs_factor = costs[model]["output"]
            input_costs = result["prompt_tokens"] * input_costs_factor / 1000000
            output_costs = result["completion_tokens"] * output_costs_factor / 1000000
            total_cost = input_costs + output_costs # Calculate total cost
            combined_results = {
                "accuracy": result["accuracy"],
                "prompt_tokens": result["prompt_tokens"],
                "completion_tokens": result["completion_tokens"],
                "duration": result["duration"],
                "cost": {
                    "input": input_costs,
                    "output": output_costs,
                    "total": total_cost, # Include total cost in the results
                }
            }
            method = ""
            if sub_folder == "io":
                method = "Zero-Shot"
            elif sub_folder == "scot":
                method = "SCoT"
            elif sub_folder == "synth_few_shot_split":
                method = "Synth. Few-Shots"
            elif sub_folder == "zero_shot_cot":
                method = "Zero-Shot CoT"

            if model == "gpt-3.5-turbo-0125":
                output_for_gpt_3_5[method].append(combined_results)
            elif model == "gpt-4-0125-preview":
                output_for_gpt_4[method].append(combined_results)

save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/charts/data/eval_prompt_method/0.2"
combined_results_for_gpt3_path = f"{save_path}/combined_results_for_gpt3.json"
combined_results_for_gpt4_path = f"{save_path}/combined_results_for_gpt4.json"

def save_results(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

save_results(combined_results_for_gpt3_path, output_for_gpt_3_5)
save_results(combined_results_for_gpt4_path, output_for_gpt_4)
