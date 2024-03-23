
# Sampling and static Prompting for code generation with manual and generated unit tests

The scripts for running the experiments are categorized based on their operational costs and functions. Scripts utilizing GPT-4 have higher expenses, typically ranging from $0.5 to $5 per execution. In contrast, those leveraging GPT-3.5-turbo are significantly more economical, generally costing less than $1 per run. Additionally, there are scripts designed for generating code and conducting unit tests. To facilitate identification, scripts have been labeled as "high costs," "low costs," or "exec" according to their associated expenses and functionalities. While all scripts were tested in a local environment and appeared to be safe, their safety cannot be guaranteed. Therefore, it is advised not to run scripts marked "exec" without employing Docker or on critical systems to mitigate risks.

# Prerequisites

Before you begin, ensure you meet the following prerequisites to avoid compatibility issues:

- **Operating System**: The experiments have been executed on WSL2. If you're using Windows, you must first install WSL2. Native Ubuntu environments or macOS should work without issues.

- **Environment Variables**: You need to create a `.env` file in the root directory of the project. This file should include your `OPENAI_API_KEY` and the `DEV_PATH`. The `DEV_PATH` must be the full path to the project directory. Here's an example:
  ```
  OPENAI_API_KEY=your_key_here
  DEV_PATH="/home/username/dev/project_name"
  ```

- **Human Eval Dataset**: The `human_eval.zip` file must be unzipped and the extracted `human_eval` folder should be placed in the `src` folder of the project.

**IMPORTANT**: Please ensure all scripts are executed from a Bash shell and that you remain in the root directory of the project. Do not alter the directory path.

---

## Setting Up Python 3 and a Virtual Environment

### Step 1: Install Python 3
Ensure you have Python 3 installed on your system. You can download it from the official Python website: [python.org](https://www.python.org/downloads/).

### Step 2: Verify Installation
Open your terminal (Command Prompt on Windows, Terminal on macOS and Linux) and type the following command to check if Python is installed:
```
python3 --version
```
This should display the Python version number.

### Step 3: Create a Virtual Environment
Navigate to your project directory in the terminal, then run the following command to create a virtual environment named `venv`:
```
python3 -m venv venv
```
This command creates a directory named `venv` where all Python packages for your project will be stored.

### Step 4: Activate the Virtual Environment

- **On macOS and Linux:**
```
source venv/bin/activate
```
After activation, your terminal prompt will change to indicate that the virtual environment is active.

### Step 5: Install the packages for this project
```pip install -r requirements.txt```

### Step 6: Deactivate the python env
```deactivate```

## Bash Scripts Access

To ensure all scripts used in the experiments are executable, follow the steps below. This grants the necessary permissions to execute the scripts.

```sh
chmod +x ./src/scripts/chmod_for_all.sh
./src/scripts/chmod_for_all.sh
```

---

# Experiment 1: Comparison between Temperatures and LLMs

## Description

This experiment aims to compare the effects of different temperatures on the performance of two different language models, specifically gpt-3.5-turbo-0125 and gpt-4-0125-preview, using a zero-shot prompting method. The experiment involves generating code solutions for all 164 HumanEval problems, evaluating the solutions for pass@k (k=1-10), and visualizing the results.

## Factors

- **Models:** gpt-3.5-turbo-0125, gpt-4-0125-preview
- **Temperatures:** 0.2, 0.4, 0.6, 0.8
- **Prompting Method:** Zero-Shot

## Execution steps

### 1.1 Generation
To evaluate for pass@k<=10 youve to execute both scripts 10 times.

#### For gpt-3.5 (low costs):

```sh
./src/scripts/gen_data/temperature/gpt_3.5/run_sampling_for_temp.sh
```

#### For gpt-4 (high costs):

```sh
./src/scripts/gen_data/temperature/gpt_4/run_sampling_for_temp.sh
```

The results will be stored at: `src/benchmark_results/code_gen/simple`

### 1.2 Data Conversion and Evaluation

To combine the code generation results into one file per model and temperature, and then evaluate the results for pass@k (k=1-10), execute the following (exec):

```sh
./src/scripts/eval_data/eval_temp/eval_temp.sh
```

After completion, the accuracy and associated data are stored at: `src/benchmark_results/results/data/temperature`

### 1.3 Visualization

This section should detail the method for visualizing the results, including any specific software or scripts used.

```sh
./src/scripts/plot_data/temperature/create_plot_for_temp.sh
```

The result is stored at: `src/benchmark_results/images/temperature`

---

# Experiment 2: Comparison between 2 types of Reflexion

## Description

This experiment aims to compare the effects of 2 types of reflexion. One were the best code-solution is kept for refinement on each iteration and another one where just the previous code-solution is being used.

## Factors

- **Models:** gpt-3.5-turbo-0125, gpt-4-0125-preview
- **Prompting Method:** Reflexion (use_best, use_next)

## Execution steps

### 2.1 Generation:
To reduce variance execute each script 5 times.

use_best with gpt-3.5 (low costs):
```sh
./src/scripts/gen_data/reflexion/use_best/gpt_3.5/run_reflexion_gpt_3.5.sh
```

use_best with gpt-4 (high costs):
```sh
./src/scripts/gen_data/reflexion/use_best/gpt_4/run_reflexion_gpt_4.sh
```

use_next with gpt-3.5 (low costs):
```sh
./src/scripts/gen_data/reflexion/use_next/gpt_3.5/run_reflexion_gpt_3.5.sh
```

use_next with gpt-4 (high costs):
```sh
./src/scripts/gen_data/reflexion/use_next/gpt_4/run_reflexion_gpt_4.sh
```

### 2.2 Data Conversion and Evaluation
The following script creates 10 files, each representing the maximum iteration count. It uses the 5 initally generated files for this (exec).

```sh
./src/scripts/eval_data/eval_reflexion/eval_reflexion.sh
```

The results will be stored at: `src/benchmark_results/results/data/eval_refl_keep_best`

### 2.3 Visualization

```sh
./src/scripts/plot_data/reflexion/create_plot_for_reflexion.sh
```

The results will be stored at: `./src/benchmark_results/images/keep_best`

# Experiment 3: Sampling with Prompting Methods

## Description

In this experiment, we delve into the effectiveness of various prompting methods in achieving pass rates of k<=10. Building upon the foundation laid in the first experiment, which focused on evaluating temperatures through Zero-Shot Prompting, we have the opportunity to extend our insights by incorporating these existing results.

## Factors

- **Models:** gpt-3.5-turbo-0125, gpt-4-0125-preview
- **Prompting Methods:** Zero-Shot, Zero-Shot Chain of Thought (CoT), Structured CoT, Synthetic Few-Shots

## Execution steps

### 3.1 Generation

To produce code solutions for the gpt-3.5-turbo-0125 model, execute the following scripts. Note that each script is designed to generate the code solutions a single time. In order to conduct an evaluation for pass rates of k<=10, it is necessary to run each script 10 times.

- For Zero-Shot Chain of Thought (CoT) generation (low costs):
```sh
./src/scripts/gen_data/sampling/gpt_3.5/run_sampling_zero_shot_cot.sh
```

- For Structured CoT generation (low costs):
```sh
./src/scripts/gen_data/sampling/gpt_3.5/run_sampling_scot.sh
```

- For Synthetic Few-Shots generation (low costs):
```sh
./src/scripts/gen_data/sampling/gpt_3.5/run_sampling_synth_few_shot.sh
```

To generate code solutions for the gpt-4-0125-preview model, follow these instructions. Each script below is tailored for a specific prompting method and needs to be executed individually to create code solutions. Similar to the gpt-3.5 model, to ensure a thorough evaluation for pass rates of k<=10, it's necessary to run each script ten times.

- For Zero-Shot Chain of Thought (CoT) generation (high costs):
```sh
./src/scripts/gen_data/sampling/gpt_4/run_sampling_zero_shot_cot.sh
```

- For Structured CoT generation (high costs):
```sh
./src/scripts/gen_data/sampling/gpt_4/run_sampling_scot.sh
```

- For Synthetic Few-Shots generation (high costs):
```sh
./src/scripts/gen_data/sampling/gpt_4/run_sampling_synth_few_shot.sh
```

### 3.2 Data Conversion and Evaluation

(exec)
```sh
./src/scripts/eval_data/eval_code_gen_per_prompt_type/eval_prompting.sh
```

Results will be stored at: `src/benchmark_results/results/data/eval_prompt_method/combined_results_prompt_method.jsonl`

### 3.3 Visualization

To visualize the data use:

```sh
./src/scripts/plot_data/prompting_methods/create_plot_for_prompting_methods.sh
```

The results will be stored at: `src/benchmark_results/images/prompt_method` 

# Experiment 4: Enhancing Unit Test Generation through Refinement

## Description

This experiment investigates two methodologies for unit test generation. The first method enhances the quality of tests by employing a refinement step, where the language model is tasked with detecting and eliminating potentially flawed tests. The second method skips this refinement, generating unit tests directly without assessing their potential flaws.

## Factors

- **Models:** gpt-3.5-turbo-0125, gpt-4-0125-preview
- **Prompting Methods:** Zero-Shot, both with and without the removal of potentially flawed test cases

## Execution steps

### 4.1 Generation

To reduce variability, each script must be executed three times.

**For gpt-3.5:**

- Generating tests with refinement (removal of potentially flawed tests) (low costs):
```sh
./src/scripts/gen_data/tests_with_removal/gpt_3.5/tests_gen_with_removal.sh
```

- Generating tests without refinement (low costs):
```sh
./src/scripts/gen_data/tests_with_removal/gpt_3.5/tests_gen_without_removal.sh
```

**For gpt-4:**

- Generating tests with refinement (high costs):
```sh
./src/scripts/gen_data/tests_with_removal/gpt_4/tests_gen_with_removal.sh
```

- Generating tests without refinement (high costs):
```sh
./src/scripts/gen_data/tests_with_removal/gpt_4/tests_gen_without_removal.sh
```

### 4.2 Conversion and Evaluation

(exec)
```sh
./src/scripts/eval_data/eval_tests/eval_tests_with_removal/eval_tests_with_removal.sh
```

Results will be stored at: `src/benchmark_results/results/data/eval_tests_refinement` 

# Experiment 5: Optimizing Solution Selection Using Generated Tests from Experiment 4

## Description

This experiment focuses on optimizing solution selection by leveraging unit tests generated in Experiment 4. For each problem, we create multiple samples and use the size of these samples to apply the generated tests, aiming to identify the most robust solution—one that passes the highest number of unit tests. This process integrates the code solutions generated in Experiment 1, employing randomized data through simulation sampling to ensure a broad and unbiased evaluation.

## Factors

- **Models:** gpt-3.5-turbo-0125, gpt-4-0125-preview
- **Prompting Methods for code-generation:** Zero-Shot
- **Tests** both the unit tests in Experiment 4 and the solutions in Experiment 1.

## Execution steps

### 5.1 Generation and Evaluation

**For gpt-3.5:**

To initiate the sampling simulation using generated tests with removal, execute the following script (exec and no costs).

```sh
./src/scripts/gen_data/sampling_simulation_with_gen_tests/sampling_for_tests_with_removal/gpt_3.5/sampling_for_tests_with_removal.sh
```

**For gpt-4:**

For conducting the sampling simulation with gpt-4, using the tests that have undergone the removal process, run this script (exec and no costs) :

```sh
./src/scripts/gen_data/sampling_simulation_with_gen_tests/sampling_for_tests_with_removal/gpt_4/sampling_for_tests_with_removal.sh
```

### 5.2 Conversion

```sh
./src/scripts/eval_data/eval_sampling_with_gen_tests/for_test_removal/eval_sampling_with_gen_tests.sh
```
Results will be stored at: `src/benchmark_results/images/test_refinement_applied`

### 5.3 Visualization

```sh
./src/scripts/plot_data/sampling_with_gen_tests_refinement/create_plot.sh
```

Results will be stored at: `src/benchmark_results/images/test_refinement_applied`

# Experiment 6: Advanced Unit Test Generation Using Prompting Methods

## Description

This experiment advances the exploration into unit test generation by applying the prompting methods trialed in Experiment 3. With an emphasis on gpt-4, this iteration incorporates test removal, a technique proven to enhance accuracy for gpt-4 in Experiment 5, thereby refining the quality of generated tests.

## Factors

- **Models:** gpt-3.5-turbo-0125, gpt-4-0125-preview
- **Prompting Methods for unit-test generation:** Zero-Shot, Zero-Shot Chain of Thought (CoT), Synthetic Few-Shots

## Execution steps

### 6.1 Generation

To ensure consistency and reduce variability, each script should be executed three times.

**For gpt-3.5-turbo:**

- Generating tests with Synthetic Few-Shots (low costs):
```sh
./src/scripts/gen_data/tests_with_prompt_methods/gpt_3.5/run_test_gen_synth_few_shot.sh
```

- Generating tests with Zero-Shot CoT (low costs):
```sh
./src/scripts/gen_data/tests_with_prompt_methods/gpt_3.5/run_test_gen_zero_shot_cot.sh
```

- Generating tests with Zero-Shot (low costs):
```sh
./src/scripts/gen_data/tests_with_prompt_methods/gpt_3.5/run_test_gen_zero_shot.sh
```

**For gpt-4:**

- Generating tests with Synthetic Few-Shots (high costs):
```sh
./src/scripts/gen_data/tests_with_prompt_methods/gpt_4/run_test_gen_synth_few_shot.sh
```

- Generating tests with Zero-Shot CoT (high costs):
```sh
./src/scripts/gen_data/tests_with_prompt_methods/gpt_4/run_test_gen_zero_shot_cot.sh
```

- Generating tests with Zero-Shot (high costs):
```sh
./src/scripts/gen_data/tests_with_prompt_methods/gpt_4/run_test_gen_zero_shot.sh
```

### 6.2 Conversion and Evaluation

(exec)
```sh
./src/scripts/eval_data/eval_tests/eval_tests_with_prompting_methods/eval_tests_with_prompting_methods.sh
```

Results will be stored at: `src/benchmark_results/results/data/eval_tests_with_methods`

# Experiment 7: 

## Description

This experiment uses the unit tests from experiment 6 for selection of code-solutions created through zero-shot prompting

## Factors

- **Models:** gpt-3.5-turbo-0125, gpt-4-0125-preview
- **Unit Tests:** Several unit-tests for each prompting method: (Zero-Shot, Zero-Shot CoT, Synth. Few-Shots) 

### 7.1 Generation and Evaluation

gpt-3.5-turbo for code generation and gpt-3.5-turbo for test generation (exec and no costs):
```sh
./src/scripts/gen_data/sampling_simulation_with_gen_tests/sampling_for_tests_with_prompting_methods/gpt_3.5/run_synth_few_shot.sh
./src/scripts/gen_data/sampling_simulation_with_gen_tests/sampling_for_tests_with_prompting_methods/gpt_3.5/run_zero_shot_cot.sh
./src/scripts/gen_data/sampling_simulation_with_gen_tests/sampling_for_tests_with_prompting_methods/gpt_3.5/run_zero_shot.sh
```

gpt-4-turbo for code generation and gpt-3.5-turbo for test generation (exec and no costs):
```sh
./src/scripts/gen_data/sampling_simulation_with_gen_tests/sampling_for_tests_with_prompting_methods/gpt_4/tests_by_gpt_3.5/run_synth_few_shot.sh
./src/scripts/gen_data/sampling_simulation_with_gen_tests/sampling_for_tests_with_prompting_methods/gpt_4/tests_by_gpt_3.5/run_zero_shot_cot.sh
./src/scripts/gen_data/sampling_simulation_with_gen_tests/sampling_for_tests_with_prompting_methods/gpt_4/tests_by_gpt_3.5/run_zero_shot.sh
```

gpt-4-turbo for code generation and gpt-4-turbo for test generation (exec and no costs):
```sh
./src/scripts/gen_data/sampling_simulation_with_gen_tests/sampling_for_tests_with_prompting_methods/gpt_4/tests_by_gpt_4/run_synth_few_shot.sh
./src/scripts/gen_data/sampling_simulation_with_gen_tests/sampling_for_tests_with_prompting_methods/gpt_4/tests_by_gpt_4/run_zero_shot_cot.sh
./src/scripts/gen_data/sampling_simulation_with_gen_tests/sampling_for_tests_with_prompting_methods/gpt_4/tests_by_gpt_4/run_zero_shot.sh
```

### 7.2 Conversion

```sh
./src/scripts/eval_data/eval_sampling_with_gen_tests/for_test_prompting_methods/eval_sampling_with_gen_tests_prompting.sh
```

Results will be stored at: `src/benchmark_results/results/data/eval_tests_with_methods_applied`

### 7.3 Visualization
```sh
./src/scripts/plot_data/sampling_with_gen_tests_prompting/create_plot.sh
```

Results will be stored at: `src/benchmark_results/images/test_methods_applied`