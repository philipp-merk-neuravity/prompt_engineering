from typing import *
from utils.data_conversion import split_tests_into_individual_functions, extract_function_name, remove_function_definition_from_test, add_typing_package_to_code_solution, remove_typing_package_from_code_solution
import multiprocessing
import functools

# def run_test_with_timeout(solution_function, test, timeout):
#     # Define a wrapper function to execute the test
#     def test_wrapper(queue, solution_code, test):
#         namespace = {}
#         exec(solution_code, namespace)  # Execute solution code in isolated namespace

#         # Extract solution function from namespace
#         function_name = extract_function_name(solution_code)
#         solution_function = namespace[function_name]

#         # Prepare test execution environment
#         test_namespace = dict(namespace)
#         exec(test, test_namespace)  # Execute test code, including check function definition

#         try:
#             # Call check function with the solution function
#             test_namespace['check'](solution_function)
#             queue.put("passed")
#         except AssertionError:
#             queue.put("failed")
#         except Exception as e:
#             error_info = f"{type(e).__name__}: {str(e)}"
#             queue.put(("error", error_info))

#     # Create a multiprocessing Queue to retrieve the result from the subprocess
#     queue = multiprocessing.Queue()

#     # Prepare the solution code for execution in the subprocess
#     solution_executable = functools.partial(test_wrapper, queue, solution_function)

#     # Wrap the test function to pass the necessary arguments
#     process = multiprocessing.Process(target=solution_executable, args=(test,))

#     # Start the process and wait for it to finish or timeout
#     process.start()
#     process.join(timeout)

#     # Determine the outcome based on whether the process finished before the timeout
#     if process.is_alive():
#         process.terminate()  # Terminate the process if it is still running
#         process.join()
#         return "timeout", "Function execution exceeded time limit"
#     else:
#         result = queue.get()  # Retrieve the result from the queue
#         return result
    
def run_test_with_timeout(solution_function, test, timeout):
    # Define a wrapper function to execute the test
    def test_wrapper(queue, solution_code, test):
        namespace = {}
        exec(solution_code, namespace)  # Execute solution code in isolated namespace

        # Extract solution function from namespace
        function_name = extract_function_name(solution_code)
        solution_function = namespace[function_name]

        # Prepare test execution environment
        test_namespace = dict(namespace)
        exec(test, test_namespace)  # Execute test code, including check function definition

        try:
            # Call check function with the solution function
            test_namespace['check'](solution_function)
            queue.put("passed")
        except AssertionError:
            queue.put("failed")
        except Exception as e:
            error_info = f"{type(e).__name__}: {str(e)}"
            queue.put(("error", error_info))

    # Create a multiprocessing Queue to retrieve the result from the subprocess
    queue = multiprocessing.Queue()

    # Prepare the solution code for execution in the subprocess
    solution_executable = functools.partial(test_wrapper, queue, solution_function, test)

    # Wrap the test function to pass the necessary arguments
    process = multiprocessing.Process(target=solution_executable)

    # Start the process and wait for it to finish or timeout
    process.start()
    process.join(timeout)

    # Determine the outcome based on whether the process finished before the timeout
    if process.is_alive():
        process.terminate()  # Terminate the process if it is still running
        process.join()
        return "timeout", "Function execution exceeded time limit"
    else:
        if process.exitcode == 0:
            # Normal exit, retrieve the result
            return queue.get()
        else:
            # Abnormal exit, interpret as potential stack overflow or other crash
            return "error", "Process terminated abnormally, potentially due to stack overflow or other critical error"


def run_tests(solution_code: str, tests: list, timeout=15):
    results = {
        "passed_tests": [],
        "failed_tests": [],
    }

    for test in tests:
        result = run_test_with_timeout(solution_code, test, timeout)
        test = remove_function_definition_from_test(test)
        if result == "passed":
            results["passed_tests"].append(test)
        elif result == "failed":
            results["failed_tests"].append(test)
        else:
            # Handle timeout or other errors
            error_type, error_info = result
            if error_type == "timeout":
                results["failed_tests"].append(("TimeoutError: Execution exceeded time limit for: " + test))
            else:
                results["failed_tests"].append((error_info + " for: " + test))

    if len(results["failed_tests"]) > 0 or len(results["failed_tests"]) > 0:
        return results, False
    else:
        return results, True
        
    

def get_test_results(code_solution: str, tests: str):
    individual_tests = split_tests_into_individual_functions(tests)
    code_solution = add_typing_package_to_code_solution(code_solution)
    return run_tests(code_solution, individual_tests)  

