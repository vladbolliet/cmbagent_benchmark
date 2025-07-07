# imports
from typing import Optional 
import json
import os
import openai
import anthropic
from getpass import getpass
import cmbagent
import re # for regex
import ast  # safe way to parse Python literals like lists, dicts
import pandas as pd
from tabulate import tabulate #for printing pretty tables in the terminal.
from dotenv import load_dotenv
import random

# Load all problems from a JSON file into a python dict

def load_problems(
    json_path: str,
    tests_dir: str,
    nb_bronze_pbs: int = 0,
    nb_silver_pbs: int = 0,
    nb_gold_pbs: int = 0,
    nb_platinum_pbs: int = 0
) -> dict:
    with open(json_path, 'r') as f:
        problems = json.load(f)

    if nb_bronze_pbs == 0 and nb_silver_pbs == 0 and nb_gold_pbs == 0 and nb_platinum_pbs == 0:
        return problems

    level_limits = {
        'bronze': min(nb_bronze_pbs, 123),
        'silver': min(nb_silver_pbs, 100),
        'gold': min(nb_gold_pbs, 63),
        'platinum': min(nb_platinum_pbs, 21),
    }

    level_groups = {'bronze': [], 'silver': [], 'gold': [], 'platinum': []}
    for key, info in problems.items():
        level = info.get('problem_level')
        if level in level_groups:
            try:
                _ = load_test_cases_for_one_problem(key, tests_dir)
                level_groups[level].append((key, info))
            except Exception as e:
                print(f"❌ Skipping {key} due to test case error: {e}")

    selected = {}
    for level, limit in level_limits.items():
        sampled = random.sample(level_groups[level], min(limit, len(level_groups[level])))
        for key, info in sampled:
            selected[key] = info

    return selected

# load_test_cases_for_one_problem as a list of tuples of lists

def load_test_cases_for_one_problem(problem_id: str, tests_dir: str) -> list | None:
    test_cases = []
    i = 1
    while True:
        input_file = os.path.join(tests_dir, problem_id, f"I.{i}")
        output_file = os.path.join(tests_dir, problem_id, f"O.{i}")

        if not os.path.exists(input_file) or not os.path.exists(output_file):
            break

        try:
            with open(input_file, "r") as f_in:
                input_list = list(map(int, f_in.read().strip().split()))

            with open(output_file, "r") as f_out:
                output_list = list(map(int, f_out.read().strip().split()))

            test_cases.append((input_list, output_list))

        except ValueError as e:
            print(f"⚠️ Skipping problem {problem_id} due to non-numeric data in test case {i}: {e}")
            return None

        i += 1
    if test_cases:
        return test_cases
    else:
        print("No test cases found")
        return None

def print_cmbagent_benchmark_summary(results_summary: dict) -> None:
    from tabulate import tabulate
    import pandas as pd

    print("\n============ BENCHMARK SUMMARY FOR CMBAGENT FOR ALL PROBLEMS ==============")

    problems_solved = 0
    #total_benchmark_time = 0
    total_problems = len(results_summary)
    total_cost_df = 0
    total_time = 0
    failed_problems_due_to_execution_limit = 0
    failed_problems_due_to_error_in_code = 0
    failed_problems_due_to_wrong_result = 0
    failed_problems_due_to_wrong_return_type = 0
    
    for problem_id, stats in results_summary.items():
        
        # print data for every problem
        
        print(f"{problem_id}:\n"
              f"  Total test cases: {stats['total']}\n"
              f"  Correctly solved test cases: {stats['correct']}\n"
              f"  Problem solved: {stats['problem_passed']}\n"
              #f"  Time to run: {stats['problem_time']}\n"
        )

        # print error information for every problem
        
        if stats['problem_passed']:
            problems_solved += 1
        else:
            print(f"problem failed due to {stats['error_code']}\n")
            if stats['error_code'] == "execution_limit_reached":
                failed_problems_due_to_execution_limit += 1
            elif stats['error_code'] == "error_in_code":
                failed_problems_due_to_error_in_code += 1
            elif stats['error_code'] == "not_int_list":
                failed_problems_due_to_wrong_return_type += 1
            elif stats['error_code'] == "wrong_answer":
                failed_problems_due_to_wrong_result += 1
                
        # get cost and time per problem (and add up)

        total_cost_df += results_summary[problem_id]['cost_and_time_dataframe']['total_planning_cost_df'] + results_summary[problem_id]['cost_and_time_dataframe']['total_control_cost_df']
        total_time += results_summary[problem_id]['cost_and_time_dataframe']['total_planning_time'] + results_summary[problem_id]['cost_and_time_dataframe']['total_control_time']

    average_accuracy = (problems_solved / total_problems) * 100 if total_problems > 0 else 0
    percentage_of_pbs_with_execution_limit_reached = (failed_problems_due_to_execution_limit/total_problems) * 100 if total_problems > 0 else 0
    percentage_of_pbs_with_wrong_result = (failed_problems_due_to_wrong_result/total_problems) * 100 if total_problems > 0 else 0
    percentage_of_pbs_with_error_in_code = (failed_problems_due_to_error_in_code/total_problems) * 100 if total_problems > 0 else 0
    percentage_of_pbs_with_wrong_return_type = (failed_problems_due_to_wrong_return_type/total_problems) * 100 if total_problems > 0 else 0

    print("============ CONCLUSION ===============")
    print(
    f"Average accuracy over all problems: {average_accuracy:.2f}%\n"
    f"Percentage of problems failed due to execution limit reached: {percentage_of_pbs_with_execution_limit_reached:.2f}%\n"
    f"Percentage of problems failed due to wrong answer in one of test cases: {percentage_of_pbs_with_wrong_result:.2f}%\n"
    f"Percentage of problems failed due to error in code OR wrong return type: {(percentage_of_pbs_with_error_in_code + percentage_of_pbs_with_wrong_return_type):.2f}%\n"
    f"Total benchmark time: {total_time:.2f}s\n"
    f"Total cost:\n{total_cost_df}\n"

)

# find result found by cmbagent through execution with regex

# def find_result_in_cmbagent_string(cmbagent_answer: dict) -> list[int] | None:
#     last_execution_output_message = None

#     for message in reversed(cmbagent_answer['chat_history']):
#         content = message.get('content', '')
#         if "Execution output:" in content:
#             last_execution_output_message = content
#             break

#     if last_execution_output_message:
#         match = re.search(r'Execution output:\s*(.*)', last_execution_output_message)
#         if match:
#             result_str = match.group(1).strip()
#             try:
#                 # Safely parse the string representation of a Python literal (like a list)
#                 result_list = ast.literal_eval(result_str)
#                 # Optional: verify it's a list of ints
#                 if isinstance(result_list, list) and all(isinstance(x, int) for x in result_list):
#                     return result_list
#                 else:
#                     print("Parsed result is not a list of ints:", result_list)
#                     return None
#             except Exception as e:
#                 print("Error parsing output string:", e)
#                 return None
#         else:
#             print("Pattern found but couldn't parse output.")
#             return None
#     else:
#         print("No execution output found in chat history.")
#         return None

def extract_code(results):
    code_str = results['final_context']['previous_steps_execution_summary']
    matches = re.findall(r"```python\n(.*?)```", code_str, re.DOTALL)
    
    if not matches:
        print("No code block found.")
        return None
    
    final_code = matches[-1].strip()
    return final_code

# run python code locally

import multiprocessing
import traceback

def _target(code_str, input_data, result_queue):
    try:
        scope = {}
        exec(code_str, scope)  # use same dict for globals and locals

        main_func = scope.get("main_function")
        if not main_func:
            result_queue.put(("error", "No function named 'main_function' found in code."))
            return

        result = main_func(input_data)
        result_queue.put(("success", result))

    except Exception as e:
        tb = traceback.format_exc()
        result_queue.put(("error", f"Exception during execution:\n{tb}"))

def run_python_code_locally_for_one_test_case(code_str: str, input_data: list[int], timeout: int = 4) -> list[int]:
    result_queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=_target, args=(code_str, input_data, result_queue))

    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()
        process.join()
        raise TimeoutError(f"Test case execution exceeded {timeout} seconds and was terminated.")

    if result_queue.empty():
        raise RuntimeError("No result returned from subprocess.")

    status, payload = result_queue.get()

    if status == "error":
        raise RuntimeError(payload)

    return payload  # success case

# main benchamrk function for cmbagent

def get_problem_cost_and_time():
    base_dir = "/mnt/p/stage/cmbagent_benchmark/python/evaluation/planning_and_control_agent/cmbagent_output"

    def listdir_no_hidden(path):
        return [f for f in os.listdir(path) if not f.startswith(".") and not os.path.basename(f).startswith(".")]

    # --- Planning Cost ---
    planning_cost_path = os.path.join(base_dir, "planning", "cost")
    planning_cost_files = listdir_no_hidden(planning_cost_path)
    planning_cost_file = planning_cost_files[0]
    with open(os.path.join(planning_cost_path, planning_cost_file)) as f:
        planning_cost_list = json.load(f)
    total_planning_cost_df = pd.DataFrame([planning_cost_list[-1]])
    total_planning_cost_df = total_planning_cost_df.select_dtypes(include='number')  # keep only numeric

    # --- Planning Time ---
    planning_time_path = os.path.join(base_dir, "planning", "time")
    planning_time_files = listdir_no_hidden(planning_time_path)
    planning_time_file = planning_time_files[0]
    with open(os.path.join(planning_time_path, planning_time_file)) as f:
        total_planning_time = json.load(f)["total_time"]

    # --- Control Cost ---
    control_cost_path = os.path.join(base_dir, "control", "cost")
    total_costs = []
    for fname in listdir_no_hidden(control_cost_path):
        with open(os.path.join(control_cost_path, fname)) as f:
            cost_list = json.load(f)
            total_costs.append(cost_list[-1])
    df = pd.DataFrame(total_costs)
    total_control_cost_df = df.drop(columns=["Agent"], errors="ignore").sum(numeric_only=True).to_frame().T

    # --- Control Time ---
    control_time_path = os.path.join(base_dir, "control", "time")
    total_control_time = 0
    for fname in listdir_no_hidden(control_time_path):
        with open(os.path.join(control_time_path, fname)) as f:
            total_control_time += json.load(f)["total_time"]

    # --- Final Output ---
    problem_cost_and_time = {
        "total_planning_cost_df": total_planning_cost_df,
        "total_planning_time": total_planning_time,
        "total_control_cost_df": total_control_cost_df,
        "total_control_time": total_control_time,
    }

    return problem_cost_and_time

def run_benchmark_on_cmbagent(problems: dict, problem_dir: str, cmbagent_model: str) -> dict:

    results_summary = {}
    all_problem_costs = []  # collect all cost DataFrames here
    skipped_problems = []

    total_problems = len(problems)
    # c = 0

    for problem_index, (problem_id, problem) in enumerate(problems.items(), start=1):

        print("===============================================================")
        print(f"\t\tEvaluating CMBAgent on problem {problem_index}/{total_problems}: {problem_id}")
        print("===============================================================")

        problem_has_passed = False
        #total_time = 0
        error_code = ""
        
        test_cases = load_test_cases_for_one_problem(problem_id, problem_dir)

        if not test_cases:
            skipped_problems.append(problem_id)
            continue

        example_input, example_output = test_cases[0]

        prompt = (
                f"Task:\n"
                f"Write python code. A function to solve the problem: {problem['description']}\n\n"
                f"Requirements:\n"
                f"- The main function must be named `main_function`, even if helper functions are needed.\n"
                # f"- Include all code inside a single <code> ... </code> block, even if you revise it.\n"
                f"- No extra text or explanation, only the code block.\n"
                f"- Execution time must stay under 4 seconds, even for large inputs.\n\n"
                f"Format:\n"
                f"- Input example: {example_input}\n"
                f"- Expected output: {example_output}\n"
                f"- Input and output are python lists. For output:\n"
                f"  - Return [n] for a single integer result.\n"
                f"  - Return [a, b, c, ...] for a list result.\n"
        )

        model_answer = cmbagent.planning_and_control_context_carryover(
                              prompt,
                              max_rounds_control = 5,
                              n_plan_reviews = 3,
                              max_n_attempts = 2,
                              max_plan_steps=5,
                              default_llm_model = "gpt-4.1-2025-04-14",
                              engineer_model = "gemini-2.5-pro-preview-03-25",
                              camb_context_model = "gemini-2.5-pro-preview-03-25",
                              researcher_model = "gpt-4.1-2025-04-14",
                              plan_reviewer_model = "claude-3-7-sonnet-20250219",
                              plan_instructions=r"""
                            Use engineer for whole analysis; at the end, provide the full final code, including only the main function (and any                              necessary helpers). The plan must have between 3 and 5 steps.
                            """
                              #restart_at_step = 1,
        )     

        # get time and cost

        problem_cost_and_time = get_problem_cost_and_time()
        
        code_str = extract_code(model_answer)
        correct = 0
        cost_dfs = []

        for i, (input_list, expected_output) in enumerate(test_cases[1:], start=1):

            total_test_cases = len(test_cases) - 1

            print(f"Executing code for TEST CASE {i}/{total_test_cases}, on problem {problem_index}/{total_problems}")

            try:
                result_from_code = run_python_code_locally_for_one_test_case(code_str, input_list)
            except TimeoutError as e:
                print(f"[TIMEOUT] Test case {i} on problem {problem_index} took too long and was terminated.\n"
                      f"Problem failed due to execution time out of limit. Skipping the rest of the test cases"
                )
                error_code = "execution_limit_reached"
                break
            except RuntimeError as e:
                print(f"[ERROR] Runtime error on test case {i} problem {problem_index}: {e}\n"
                      f"Problem failed due to error in code. Skipping the rest of the test cases"
                )
                error_code = "error_in_code"
                break

            if not (isinstance(result_from_code, list) and all(isinstance(item, int) for item in result_from_code)):
                print(f"Result for TEST CASE ({i}/{total_test_cases}), on problem ({problem_index}/{total_problems}) is NOT an int list"
                      f"Problem failed. Skipping the rest of the test cases."
                     )
                error_code = "not_int_list"
                break
                

            if result_from_code == expected_output:
                correct += 1
            else:
                print(f"Result for TEST CASE ({i}/{total_test_cases}), on problem ({problem_index}/{total_problems}) was WRONG.\n"
                      f"Problem failed. Skipping the rest of the test cases."
                )
                error_code = "wrong_answer"
                break

        # end of test cases' "for"

        if total_test_cases == correct:
            problem_has_passed = True

        print(f"\n =========== BENCHMARK RESULT FOR CMBAGENT ON PROBLEM {problem_id} ============\n")
        print(f"Total test cases: {total_test_cases}")
        print(f"Correctly guessed test_cases: {correct}")
        print(f"Problem solved: {problem_has_passed}")

        # saving problem info

        results_summary[problem_id] = {
            "total": total_test_cases,
            "correct": correct,
            "problem_passed": problem_has_passed,
            "error_code": error_code,
            "cost_and_time_dataframe": problem_cost_and_time
        }

        # c += 1
        # if c == 5:
        #     break

    print("⚠️ Skipped problems due to non-numeric data (or no test cases):")
    for pid in skipped_problems:
        print(f"- {pid}")

    return results_summary

# main wrapper function (this one is called by user and 'does all the work')

def run_benchmark(
    problem_json: str,
    problem_dir: str, 
    bronze_pbs: int = 0,
    silver_pbs: int = 0,
    gold_pbs: int = 0,
    platinum_pbs: int = 0,
    eval_cmbagent: bool = True, 
    cmbagent_model: Optional[str] = None,
    eval_normal_llm: bool = False, 
    llm_model: Optional[str] = None
) :

    """
    Run benchmark evaluations on problems located in problem_dir.

    Args:
        problem_dir (str): Path to the directory containing problems and test data.
        eval_cmbagent (bool): Whether to evaluate cmbagent model.
        eval_normal_llm (bool): Whether to evaluate a normal LLM.
        llm_model (Optional[str]): The normal LLM model name (required if eval_normal_llm is True).

    Returns:
        None
    """

    load_dotenv(dotenv_path="/mnt/p/stage/cmbagent_benchmark/.env", override=True)

    # Validate arguments

    if not eval_cmbagent and not eval_normal_llm:
        raise ValueError("At least one of eval_cmbagent or eval_normal_llm must be True")
    if eval_normal_llm and not llm_model:
        raise ValueError("llm_model must be provided if eval_normal_llm is True")
    if not problem_json or not problem_dir:
        raise ValueError("Both problem_json and problem_dir must be specified")
    if not os.path.exists(problem_json):
        raise FileNotFoundError(f"Problem JSON file not found: {problem_json}")
    if not os.path.exists(problem_dir):
        raise FileNotFoundError(f"Problem directory not found: {problem_dir}")
    if eval_cmbagent and not cmbagent_model:
        raise ValueError("cmbagent_model must be provided if eval_cmbagent is True")

    # get API KEYs
    
    #os.environ['OPENAI_API_KEY'] = getpass('Enter your OpenAI API key: ')
    openai.api_key = os.getenv("OPENAI_API_KEY")
    anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/mnt/p/stage/camels-453517-7c2faf50eda2.json"

    # Load problems

    problems = load_problems(problem_json, problem_dir, bronze_pbs, silver_pbs, gold_pbs, platinum_pbs)

    # evaluate cmbagent on problems

    if eval_cmbagent: 
        resultscmb = run_benchmark_on_cmbagent(problems, problem_dir, cmbagent_model)
        print_cmbagent_benchmark_summary(resultscmb)


    # evaluate the normal LLM on problems

    if eval_normal_llm:
        run_benchmark_on_normal_llm(problems, problem_dir, llm_model)

    # Print or save benchmark results

    if eval_cmbagent and not eval_normal_llm:
        return resultscmb
    if not eval_cmbagent and eval_normal_llm:
        return resultsllm
    if eval_cmbagent and eval_normal_llm:
        return resultscmb, resultsllm

    print("Benchmark evaluation completed.")

    return resultscmb