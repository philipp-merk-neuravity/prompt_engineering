# Import necessary library
import pandas as pd
import json

# Your data goes here; assume it's named `data` and already imported
path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_gen_tests/reflection/combined_results.jsonl"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_gen_tests/reflection"

with open(path, "r") as f:
    data = [json.loads(line) for line in f]

for item in data:
    item['accuracy_pass@1'] = round(item['accuracy']['pass@1'], 2)

# Convert data into a DataFrame
df = pd.DataFrame(data)

# Use pivot_table to create the table with 'model', 'reflection_type' as rows, 'iteration' as columns
pivot_table = df.pivot_table(index=['model', 'reflection_type'], columns='iteration', values='accuracy_pass@1', aggfunc='first')

# Convert pivot table to LaTeX format, with 'float_format' to ensure the rounding is applied
latex_table = pivot_table.to_latex(float_format="%.3f")

# Save or print the LaTeX table
with open(f"{save_path}/latex_table.tex", "w") as f:
    f.write(latex_table)

