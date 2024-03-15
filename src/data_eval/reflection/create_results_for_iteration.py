import json
import os

base_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/reflection"

mapping = {
    "simple_simple": {
        "0.8_0.8": {
           "gpt-3.5-turbo-0125": {
              "use_next": ["predefined"],
              "use_best": ["predefined"]
           }
        },
        "0.8_0.6": {
            "gpt-4-0125-preview": {
                "use_next": ["predefined"],
                "use_best": ["predefined"]
            }
        },
    }
}

results = []

def get_item_for_round(iteration_states, round):
    current_item = None
    for item in iteration_states:
        if item["iteration"] <= round:
            current_item = item
    return current_item

for method, temp_model_mapping in mapping.items():
    for temp, models in temp_model_mapping.items():
        for model, reflection_types in models.items():
            for reflection_type, test_types in reflection_types.items():
                for test_type in test_types:
                    current_path = f"{base_path}/{method}/{temp}/{model}/{reflection_type}/{test_type}"
                    max_iterations = 10
                    max_items = 5
                    items_for_iteration_all = {
                        0: [],
                        1: [],
                        2: [],
                        3: [],
                        4: [],
                        5: [],
                        6: [],
                        7: [],
                        8: [],
                        9: []
                    }
                    for i in range(max_items):
                        current_file_i = f"{current_path}/{i}/{i}.jsonl"
                        current_file_i_content = []
                        with open(current_file_i, "r") as f:
                            for line in f:
                                current_file_i_content.append(json.loads(line))
                        for i in range(max_iterations):
                            items_for_iteration = []
                            for item in current_file_i_content:
                                iteration_states = item["iteration_states"]
                                best_item_for_round_i = get_item_for_round(iteration_states, i)
                                if best_item_for_round_i is not None:
                                    best_item_for_round_i["task_id"] = item["task_id"]
                                    items_for_iteration.append(best_item_for_round_i)
                            items_for_iteration_all[i].extend(items_for_iteration)
                    # save to current path
                    for i in range(10):
                        k = i + 1
                        current_file_i = f"{current_path}/results_for_10/{k}/combined_results.jsonl"
                        os.makedirs(os.path.dirname(current_file_i), exist_ok=True)
                        # create the file first
                        with open(current_file_i, "w") as f:
                            # write the content
                            for item in items_for_iteration_all[i]:
                                f.write(json.dumps(item) + "\n")

