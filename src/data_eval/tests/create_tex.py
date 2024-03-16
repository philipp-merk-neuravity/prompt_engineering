import json
import pandas as pd

path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_tests/test_results_with_costs.json"  
save_path = "/home/neuravity/dev/prompt_engineering/src/benchmark_results/results/data/eval_tests"  

with open(path, "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

dfs = {model: df[df["model"] == model] for model in df["model"].unique()}

def df_to_latex(df, filename, index='model', columns='refinement_model'):
    
    selected_df = df[[index, columns, 'accuracy', 'total_cost']]
    
    latex_str = selected_df.to_latex(index=False, float_format="{:0.2f}".format, 
                                      header=["Model", "Refinement Model", "Accuracy", "Costs"])
    with open(f"{save_path}/{filename}_latex_table.tex", "w") as f:
        f.write(latex_str)

for model, model_df in dfs.items():
    df_to_latex(model_df, model)
