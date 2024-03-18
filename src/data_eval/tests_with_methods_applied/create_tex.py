import json
import pandas as pd

path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_tests_with_methods_applied/combined_results.jsonl"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_tests_with_methods_applied/eval_tests_with_methods_applied.tex"

data = []
with open(path, "r") as f:
    for line in f:
        data.append(json.loads(line))

df = pd.DataFrame(data)

df['model_test_combination'] = df['prompt_model'] + " - " + df['test_name']

pivot_df = df.pivot_table(index='model_test_combination', columns='sample_size', values='accuracy', aggfunc='mean')

def df_to_latex(df, save_path):
    df.columns = df.columns.astype(str)
    latex_code = df.to_latex(float_format="{:0.3f}".format, na_rep='--')
    with open(save_path, "w") as f:
        f.write(latex_code)

df_to_latex(pivot_df, save_path)
