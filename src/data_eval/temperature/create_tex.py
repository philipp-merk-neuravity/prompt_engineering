import json
import pandas as pd

path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/temperature/results_temp.jsonl"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/temperature"

with open(path, "r") as f:
    data = [json.loads(line) for line in f]

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(data)

# Split the DataFrame into separate DataFrames for each model
dfs = {model: df[df["model"] == model] for model in df["model"].unique()}

# Function to convert a DataFrame to a LaTeX table
def df_to_latex(df, index, columns):
    # Pivot the DataFrame to get the desired shape
    pivot_df = df.pivot(index=index, columns=columns, values='accuracy')
    # Convert the pivoted DataFrame to LaTeX
    return pivot_df.to_latex(float_format="{:0.2f}".format)

# Generate and print LaTeX tables for each model
for model, model_df in dfs.items():
    latex_table = df_to_latex(model_df, 'temp', 'k')
    with open(f"{save_path}/{model}_latex_table.tex", "w") as f:
        f.write(latex_table)