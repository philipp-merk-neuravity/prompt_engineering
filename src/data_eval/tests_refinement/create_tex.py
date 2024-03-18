import json
import pandas as pd

path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_tests/combined_results.json"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_tests/test_results.tex"

with open(path, "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Creating a new column for 'with_refinement' based on the 'test_type'
df['with_refinement'] = df['test_type'].apply(lambda x: 'Yes' if x == 'with_refinement' else 'No')

# Grouping data by 'model' and 'with_refinement', and getting the mean accuracy
grouped_df = df.groupby(['model', 'with_refinement'])['accuracy'].mean().unstack()

def df_to_latex(df, save_path):
    latex_code = df.to_latex(float_format="{:0.3f}".format, header=['With Refinement', 'Without Refinement'], index=True)
    with open(save_path, "w") as f:
        f.write(latex_code)


df_to_latex(grouped_df, save_path)