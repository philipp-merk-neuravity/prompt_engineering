import os
from dotenv import load_dotenv

load_dotenv()
# Fetch the environment variable 'DEV_PATH' defined in your system
DEV_PATH = os.getenv('DEV_PATH')


path_for_reflection = f"{DEV_PATH}/src/benchmark_results/results/data/eval_refl_keep_best/combined_results.jsonl"

mapping = [
    {
        "name": "reflection",
        "model": "gpt-3.5-turbo-0125",
        "reflection_type": "use_next"
    },
    {
        "name": "reflection",
        "model": "gpt-4-0125-preview",
        "reflection_type": "use_next"
    }
]

