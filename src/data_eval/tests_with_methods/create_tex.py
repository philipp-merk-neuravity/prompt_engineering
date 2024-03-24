import pandas as pd
import json
import os

# Fetch the environment variable 'DEV_PATH' defined in your system
DEV_PATH = os.getenv('DEV_PATH')


path = f"{DEV_PATH}/src/benchmark_results/results/data/eval_tests_with_methods/combined_mean_results.jsonl"
save_path = f'{DEV_PATH}/src/benchmark_results/results/data/eval_tests_with_methods'

with open(path, "r") as f:
    data = [json.loads(line) for line in f]

df = pd.DataFrame(data)

def df_to_latex(df, index, columns, values):
    pivot_df = df.pivot(index=index, columns=columns, values=values)
    return pivot_df.to_latex(index=True, float_format="{:0.3f}".format)

latex_table = df_to_latex(df, 'model', 'prompt_method', 'accuracy')

filename = f"{save_path}/latex_table.tex"

with open(filename, "w") as file:
    file.write(latex_table)
