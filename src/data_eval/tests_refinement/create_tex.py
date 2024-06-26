import json
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
# Fetch the environment variable 'DEV_PATH' defined in your system
DEV_PATH = os.getenv('DEV_PATH')


path = f"{DEV_PATH}/src/benchmark_results/results/data/eval_tests_refinement/combined_results_mean.jsonl"
save_path = f"{DEV_PATH}/src/benchmark_results/results/data/eval_tests_refinement"

with open(path, "r") as f:
    data = [json.loads(line) for line in f]

df = pd.DataFrame(data)

# Creating a new column for 'with_refinement' based on the 'test_type'
df['with_refinement'] = df['refinement'].apply(lambda x: 'Yes' if x == 'with_refinement' else 'No')

# Grouping data by 'model' and 'with_refinement', and getting the mean accuracy
grouped_df = df.groupby(['model', 'with_refinement'])['accuracy'].mean().unstack()

def df_to_latex(df, save_path):
    latex_code = df.to_latex(float_format="{:0.3f}".format, header=['With Refinement', 'Without Refinement'], index=True)
    with open(f"{save_path}combined_results_mean.tex", "w") as f:
        f.write(latex_code)


df_to_latex(grouped_df, save_path)