
from enum import Enum
import pathlib
import importlib.util
import re
import os

class ExecutionStatus(Enum):
    """Status of code execution"""
    SUCCESS = "success"
    TIMEOUT = "timeout"
    RUNTIME_ERROR = "runtime_error"
    COMPILATION_ERROR = "compilation_error"
    WRONG_ANSWER = "wrong_answer"
    SYSTEM_ERROR = "system_error"

def run_test_cases(generated_code: str, test_cases_folder_path: pathlib.Path) -> dict:
    import multiprocessing
    def run_main_function_in_subprocess(main_function, input_data, queue):
        try:
            result = main_function(input_data)
            queue.put(("success", result))
        except Exception as e:
            queue.put(("error", str(e)))

    TIMEOUT_SECONDS = 20
    """
    Run the generated code against all test cases in the specified folder.

    Args:
        generated_code (str): The code to be executed.
        test_cases_folder_path (pathlib.Path): Path to the folder containing test cases.
    Result format:
        {
            "status": ExecutionStatus,
            "failed_on_test_case": int | None,
        }
    """

    # Detect test case format
    files = [f.name for f in test_cases_folder_path.iterdir() if f.is_file()]
    i_files = sorted([f for f in files if re.match(r'I\.\d+$', f)])
    o_files = sorted([f for f in files if re.match(r'O\.\d+$', f)])
    in_files = sorted([f for f in files if f.endswith('.in')])
    out_files = sorted([f for f in files if f.endswith('.out')])

    if i_files and o_files:
        test_pairs = [(test_cases_folder_path / i, test_cases_folder_path / ('O.' + i.split('.')[-1])) for i in i_files]
    elif in_files and out_files:
        test_pairs = [(test_cases_folder_path / f, test_cases_folder_path / (f.replace('.in', '.out'))) for f in in_files]
    else:
        return {
            "status": ExecutionStatus.SYSTEM_ERROR.value,
            "failed_on_test_case": None,
            "error_description": "Test case format not recognized."
        }

    # Prepare to execute code
    # Write code to temp file/module
    temp_code_path = test_cases_folder_path / "_temp_main_function.py"
    with open(temp_code_path, "w") as f:
        f.write(generated_code)

    # Load main_function from temp module
    spec = importlib.util.spec_from_file_location("temp_main_module", temp_code_path)
    temp_module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(temp_module)
        main_function = getattr(temp_module, "main_function")
    except Exception as e:
        os.remove(temp_code_path)
        return {
            "status": ExecutionStatus.COMPILATION_ERROR.value,
            "failed_on_test_case": None,
            "error_description": f"Compilation error: {e}"
        }

    # Run each test case one by one
    for idx, (input_path, output_path) in enumerate(test_pairs):
        try:
            # Read and parse input
            with open(input_path, "r") as f:
                input_lines = f.read().splitlines()
            input_data = []
            for line in input_lines:
                elements = []
                for item in re.findall(r'"[^"]*"|\S+', line):
                    if item.startswith('"') and item.endswith('"'):
                        elements.append(item[1:-1])
                    else:
                        try:
                            elements.append(int(item))
                        except ValueError:
                            elements.append(item)
                input_data.append(elements)

            # Read and parse expected output
            with open(output_path, "r") as f:
                output_lines = f.read().splitlines()
            expected_output = []
            for line in output_lines:
                elements = []
                for item in re.findall(r'"[^"]*"|\S+', line):
                    if item.startswith('"') and item.endswith('"'):
                        elements.append(item[1:-1])
                    else:
                        try:
                            elements.append(int(item))
                        except ValueError:
                            elements.append(item)
                expected_output.append(elements)

            # Run main_function with timeout
            queue = multiprocessing.Queue()
            p = multiprocessing.Process(target=run_main_function_in_subprocess, args=(main_function, input_data, queue))
            p.start()
            p.join(TIMEOUT_SECONDS)
            if p.is_alive():
                p.terminate()
                p.join()
                os.remove(temp_code_path)
                return {
                    "status": ExecutionStatus.TIMEOUT.value,
                    "failed_on_test_case": idx,
                    "error_description": f"Timeout after {TIMEOUT_SECONDS} seconds"
                }
            if not queue.empty():
                status, result_or_error = queue.get()
                if status == "error":
                    os.remove(temp_code_path)
                    return {
                        "status": ExecutionStatus.RUNTIME_ERROR.value,
                        "failed_on_test_case": idx,
                        "error_description": f"Runtime error: {result_or_error}"
                    }
                result = result_or_error
            else:
                os.remove(temp_code_path)
                return {
                    "status": ExecutionStatus.SYSTEM_ERROR.value,
                    "failed_on_test_case": idx,
                    "error_description": "No result returned from subprocess."
                }

            # Compare result to expected output
            if result != expected_output:
                os.remove(temp_code_path)
                return {
                    "status": ExecutionStatus.WRONG_ANSWER.value,
                    "failed_on_test_case": idx,
                    "error_description": f"Wrong answer. Output: {result}, Expected: {expected_output}"
                }
        except Exception as e:
            os.remove(temp_code_path)
            return {
                "status": ExecutionStatus.SYSTEM_ERROR.value,
                "failed_on_test_case": idx,
                "error_description": f"System error: {e}"
            }

    os.remove(temp_code_path)
    return {"status": ExecutionStatus.SUCCESS.value, "failed_on_test_case": None}

   