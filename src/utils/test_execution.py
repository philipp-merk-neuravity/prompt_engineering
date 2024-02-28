import asyncio
import ast


def extract_function_name(code: str) -> str:
    tree = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            return node.name  # Return the name of the first top-level function

    raise ValueError("No function definition found in the provided code.")

async def get_test_results_async(code_solution: str, test_cases: list):
    function_name = extract_function_name(code_solution)
    modified_test_cases = [test_case.replace("candidate", function_name) for test_case in test_cases]
    namespace = {}
    exec("from typing import *\n" + code_solution, namespace)

    async def run_test_case(test_case_str):
        try:
            # Convert the synchronous exec() call into something that can be awaited using asyncio
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, exec, test_case_str, namespace)
            return True, test_case_str
        # except AssertionError:
        #     return False, test_case_str + " (AssertionError)"
        except Exception as e:
            return False, test_case_str + f" ({type(e).__name__}: {str(e)})"

    test_results = await asyncio.gather(*(run_test_case(test_case) for test_case in modified_test_cases))
    passed_tests = [result for result in test_results if result[0]]
    failed_tests = [result for result in test_results if not result[0]]
    is_solved = len(passed_tests) == len(modified_test_cases)
    return {"passed_tests": [pt[1] for pt in passed_tests], "failed_tests": [ft[1] for ft in failed_tests]}, is_solved

async def get_test_results_2(code_solution: str, test_cases: list):
    namespace = {}
    exec("from typing import *\n" + code_solution, namespace)

    async def run_test_case(test_case_str):
        try:
            # Convert the synchronous exec() call into something that can be awaited using asyncio
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, exec, test_case_str, namespace)
            return True, test_case_str
        # except AssertionError:
        #     return False, test_case_str + " (AssertionError)"
        except Exception as e:
            return False, test_case_str + f" ({type(e).__name__}: {str(e)})"

    test_results = await asyncio.gather(*(run_test_case(test_case) for test_case in test_cases))
    passed_tests = [result for result in test_results if result[0]]
    failed_tests = [result for result in test_results if not result[0]]
    is_solved = len(passed_tests) == len(test_cases)
    return {"passed_tests": [pt[1] for pt in passed_tests], "failed_tests": [ft[1] for ft in failed_tests]}, is_solved

from typing import *
import multiprocessing

def check_test_accuracy(code_solution: str, test_cases: list):
    def run_test_case(test_case_str):
        namespace = {}
        exec("from typing import *\n" + code_solution, namespace)
        try:
            exec(test_case_str, namespace)
            return True, test_case_str
        except Exception as e:
            return False, test_case_str + f" ({type(e).__name__}: {str(e)})"

    def run_test_case_with_timeout(test_case_str, timeout=10):
        # Create a Queue to hold the result
        queue = multiprocessing.Queue()

        # Define a wrapper function to run the test case and put the result in the queue
        def wrapper():
            result = run_test_case(test_case_str)
            queue.put(result)

        # Create and start a Process to run the wrapper function
        process = multiprocessing.Process(target=wrapper)
        process.start()

        # Wait for the process to finish or timeout
        process.join(timeout)

        # Check if the process is still alive (meaning it has timed out)
        if process.is_alive():
            process.terminate()  # Terminate the process
            process.join()  # Ensure it has cleaned up properly
            return False, test_case_str + " (TimeoutError: Test case execution exceeded 10 seconds)"

        # If the process finished within the timeout, return its result
        return queue.get()

    # Process each test case synchronously with a timeout
    test_results = [run_test_case_with_timeout(test_case) for test_case in test_cases]
    passed_tests = [result for result in test_results if result[0]]
    failed_tests = [result for result in test_results if not result[0]]
    is_solved = len(passed_tests) == len(test_cases)
    return {"passed_tests": [pt[1] for pt in passed_tests], "failed_tests": [ft[1] for ft in failed_tests]}, is_solved
