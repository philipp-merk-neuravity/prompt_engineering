import pandas as pd
import json

path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_prompt_method/combined_results.jsonl"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_prompt_method"

with open(path, "r") as f:
    data = [json.loads(line) for line in f]

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(data)

# Ensure "k" is treated as a categorical variable for sorting in the tables
df['k'] = pd.Categorical(df['k'], ordered=True)

# Function to convert a DataFrame to a LaTeX table, customized for our data structure
def df_to_latex(df, index, columns, values):
    # Pivot the DataFrame to get the desired shape with specified rows (index) and columns
    pivot_df = df.pivot(index=index, columns=columns, values=values)
    # Convert the pivoted DataFrame to LaTeX format
    return pivot_df.to_latex(index=True, float_format="{:0.3f}".format)

# Split the DataFrame into separate DataFrames for each model
models = df['model'].unique()

for model in models:
    model_df = df[df['model'] == model]
    # Generate LaTeX table for the current model
    latex_table = df_to_latex(model_df, 'method', 'k', 'accuracy')
    # Define the filename based on the model name
    filename = f"{save_path}/{model}_latex_table.tex"
    # Save the LaTeX table to a file
    with open(filename, "w") as f:
        f.write(latex_table)