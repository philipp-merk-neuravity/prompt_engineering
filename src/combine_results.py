import argparse
import json
from utils.storage import load_benchmark_results

def combine_benchmark_results(path):
    combined_results = []
    for i in range(10):
        current_path = f"{path}/{i}/{i}.jsonl"
        combined_results.extend(load_benchmark_results(current_path))

    with open(f"{path}/combined_results.jsonl", 'w') as file:
        for result in combined_results:
            file.write(json.dumps(result) + '\n')

def main():
    parser = argparse.ArgumentParser(description='Combine benchmark results from JSONL files.')
    parser.add_argument('--path', type=str, help='The base path to the benchmark results', required=True)
    args = parser.parse_args()
    combine_benchmark_results(args.path)

if __name__ == '__main__':
    main()
