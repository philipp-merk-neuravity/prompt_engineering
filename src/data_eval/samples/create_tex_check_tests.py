import json
import pandas as pd

path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_tests_with_samples/combined_samples.jsonl"
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_tests_with_samples"

with open(path, "r") as f:
    data = [json.loads(line) for line in f]

df = pd.DataFrame(data)
pivot_df = df.pivot_table(index=['model', 'test_type'], columns='sample_size', values='accuracy', aggfunc='first')

latex_code = pivot_df.to_latex(float_format="{:0.3f}".format)

latex_file_path = f"{save_path}/model_test_type_accuracy_table.tex"
with open(latex_file_path, "w") as f:
    f.write(latex_code)
