import subprocess
import json

# Define the path to the script you want to run
script_path = "/home/neuravity/dev/prompt_engineering/src/human_eval/human_eval/evaluate_functional_correctness.py"
problem_file_path="/home/neuravity/dev/prompt_engineering/src/human_eval/data/HumanEval.jsonl"
base_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/all/simple"

mapping = {
    "0.2": {
        "io": ["gpt-3.5-turbo-0125", "gpt-4-0125-preview"],
    },
    "0.4": {
        "io": ["gpt-3.5-turbo-0125", "gpt-4-0125-preview"],
    },
    "0.6": {
        "io": ["gpt-3.5-turbo-0125", "gpt-4-0125-preview"],
        "scot": ["gpt-4-0125-preview"],
        "synth_few_shot_split": ["gpt-4-0125-preview"],
        "zero_shot_cot": ["gpt-4-0125-preview"],
    },
    "0.8": {
        "io": ["gpt-3.5-turbo-0125", "gpt-4-0125-preview"],
        "scot": ["gpt-3.5-turbo-0125"],
        "synth_few_shot_split": ["gpt-3.5-turbo-0125"],
        "zero_shot_cot": ["gpt-3.5-turbo-0125"],
    }
}


for temp, method_model_mapping in mapping.items():
    for method, models in method_model_mapping.items():
        for model in models:
            combined_results = []
            samples_path = f"{base_path}/{temp}/{method}/{model}"
            samples_combined_results_path = f"{samples_path}/combined_results.jsonl"
            for i in range(10):
                k = i + 1
                current_data_path = f"{samples_path}/{i}/{i}.jsonl"
                with open(current_data_path) as f:
                    data = f.readlines()
                    combined_results.extend(data)
            # save the combined results to a file
            
            with open(samples_combined_results_path, "w") as f:
                f.writelines(combined_results)
                
            # run the evaluation script for combined results
            for i in range(10):
                k = i + 1
                command = [
                    "python", script_path,
                    "--sample_file", samples_combined_results_path,
                    "--problem_file", problem_file_path,
                    "--k", str(k),
                    # Include other command line arguments as needed
                ]
                subprocess.run(command)
                # after process is done, move the new {k}_stats.json and {k}_results.jsonl to samples_path/{i}
                save_path = f"{samples_path}/{i}"
                stats_path = f"{samples_path}/{k}_stats.json"
                results_path = f"{samples_path}/{k}_results.jsonl"

                subprocess.run(["mv", stats_path, save_path])
                subprocess.run(["mv", results_path, save_path])

            


