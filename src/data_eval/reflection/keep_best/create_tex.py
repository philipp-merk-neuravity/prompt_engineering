# Import necessary library
import pandas as pd
import json
import os

# Fetch the environment variable 'DEV_PATH' defined in your system
DEV_PATH = os.getenv('DEV_PATH')


# Your data goes here; assume it's named `data` and already imported
path = f"{DEV_PATH}/src/benchmark_results/results/data/eval_refl_keep_best/combined_results.jsonl"
save_path = f"{DEV_PATH}/src/benchmark_results/results/data/eval_refl_keep_best"

with open(path, "r") as f:
    data = [json.loads(line) for line in f]

for item in data:
    item['accuracy_pass@1'] = item['accuracy']['pass@1']

df = pd.DataFrame(data)

pivot_table = df.pivot_table(index=['model', 'reflection_type'], columns='iteration', values='accuracy_pass@1', aggfunc='first')

pivot_table_rounded = pivot_table.applymap(lambda x: round(x, 3))

latex_table = pivot_table_rounded.to_latex()
with open(f"{save_path}/latex_table.tex", "w") as f:
    f.write(latex_table)