import json
import pandas as pd

path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_tests_with_prompt_methods/combined_results.json"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_tests_with_prompt_methods"

with open(path, "r") as f:
    data = json.load(f)

df_data = []
for entry in data:
    row = {
        "model": entry["model"],
        "prompt_method": entry["prompt_method"],
        "accuracy": entry["data"]["accuracy"]
    }
    df_data.append(row)

df = pd.DataFrame(df_data)
sorted_df = df.sort_values(by=["model", "prompt_method"])

latex_code = sorted_df.to_latex(index=False, float_format="{:0.3f}".format, columns=["model", "prompt_method", "accuracy"], header=["Model", "Prompt Method", "Accuracy"])

with open(f"{save_path}/combined_results.tex", "w") as f:
    f.write(latex_code)