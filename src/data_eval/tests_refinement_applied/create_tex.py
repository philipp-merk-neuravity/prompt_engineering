import json
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
# Fetch the environment variable 'DEV_PATH' defined in your system
DEV_PATH = os.getenv('DEV_PATH')


# Function to load and prepare your data
def load_and_prepare_data(path):
    with open(path, "r") as f:
        data = [json.loads(line) for line in f]

    df = pd.DataFrame(data)

    # Convert sample_size to integer if it's a string
    df['sample_size'] = df['sample_size'].astype(int)

    # Ensure 'model', 'test_type', and 'sample_size' are included in the DataFrame
    assert {'model', 'test_type', 'sample_size'}.issubset(df.columns), "DataFrame missing required columns"

    return df

# Function to aggregate data by model, test_type, and sample size
def aggregate_data(df):
    # Aggregating data by model, test_type, and sample size
    # Adjust aggregation as necessary, e.g., mean, sum
    aggregated_df = df.groupby(['model', 'test_type', 'sample_size']).agg({'accuracy':'mean'}).reset_index()

    # Pivot table to reorganize data for LaTeX output
    pivot_df = aggregated_df.pivot_table(index=['model', 'test_type'], columns='sample_size', values='accuracy')

    return pivot_df

# Function to convert DataFrame to LaTeX and save
def df_to_latex(df, save_path, file_name="aggregated_results.tex"):
    latex_code = df.to_latex(float_format="{:0.3f}".format)
    with open(f"{save_path}/{file_name}", "w") as f:
        f.write(latex_code)

# Main function to orchestrate data loading, processing, and LaTeX conversion
def main():
    path = f"{DEV_PATH}/src/benchmark_results/results/data/eval_tests_refinement_applied/combined_stats.jsonl"
    save_path = f"{DEV_PATH}/src/benchmark_results/results/data/eval_tests_refinement_applied"

    df = load_and_prepare_data(path)
    aggregated_df = aggregate_data(df)
    df_to_latex(aggregated_df, save_path)

if __name__ == "__main__":
    main()