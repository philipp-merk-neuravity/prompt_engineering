import pandas as pd
import json

path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_tests_with_methods/combined_results.json"
save_path = '/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_tests_with_methods'

with open(path, "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

def df_to_latex(df, index, columns, values):
    pivot_df = df.pivot(index=index, columns=columns, values=values)
    return pivot_df.to_latex(index=True, float_format="{:0.3f}".format)

latex_table = df_to_latex(df, 'model', 'method', 'accuracy')

filename = f"{save_path}/latex_table.tex"

with open(filename, "w") as file:
    file.write(latex_table)
