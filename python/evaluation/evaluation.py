# THIS PYTHON FILE WAS CONVERTED FROM A VERSION OF evaluatino.ipynb WITH 'nbconvert'

#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


# get API KEYs

#os.environ['OPENAI_API_KEY'] = getpass('Enter your OpenAI API key: ')
openai.api_key = os.getenv("OPENAI_API_KEY")
anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/mnt/p/stage/camels-453517-7c2faf50eda2.json"


# In[3]:


# essential functions


# In[4]:


# Load all problems from a JSON file into a python dict

def load_problems(json_path: str) -> dict: 
    with open(json_path, 'r') as f:
        problems = json.load(f)
    return problems


# In[5]:


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


# In[6]:


def print_cmbagent_benchmark_summary(results_summary: dict) -> None:
    from tabulate import tabulate
    import pandas as pd

    print("\n============ BENCHMARK SUMMARY FOR CMBAGENT FOR ALL PROBLEMS ==============")

    problems_solved = 0
    total_benchmark_time = 0
    total_problems = len(results_summary)
    all_costs = []
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
              f"  Time to run: {stats['problem_time']}\n"
        )

        # print error information for every problem

        # save data for benchamrk conclusion
        
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
            
        total_benchmark_time += stats['problem_time']
        
        cost_df = stats.get("cost_dataframe")
        if isinstance(cost_df, pd.DataFrame) and not cost_df.empty:
            all_costs.append(cost_df[cost_df["Agent"] != "Total"])  # only agent-level rows

    average_accuracy = (problems_solved / total_problems) * 100 if total_problems > 0 else 0
    percentage_of_pbs_with_execution_limit_reached = (failed_problems_due_to_execution_limit/total_problems) * 100 if total_problems > 0 else 0
    percentage_of_pbs_with_wrong_result = (failed_problems_due_to_wrong_result/total_problems) * 100 if total_problems > 0 else 0
    percentage_of_pbs_with_error_in_code = (failed_problems_due_to_error_in_code/total_problems) * 100 if total_problems > 0 else 0
    percentage_of_pbs_with_wrong_return_type = (failed_problems_due_to_wrong_return_type/total_problems) * 100 if total_problems > 0 else 0

    print("============ CONCLUSION ===============")
    print(
    f"Average accuracy over all problems: {average_accuracy:.2f}%\n"
    f"Total benchmark time: {total_benchmark_time:.2f}s\n"
    f"Percentage of problems failed due to execution limit reached: {percentage_of_pbs_with_execution_limit_reached:.2f}%\n"
    f"Percentage of problems failed due to wrong answer in one of test cases: {percentage_of_pbs_with_wrong_result:.2f}%\n"
    f"Percentage of problems failed due to error in code OR wrong return type: {(percentage_of_pbs_with_error_in_code + percentage_of_pbs_with_wrong_return_type):.2f}%"
)
    print("=======================================")

    # Final benchmark-wide cost aggregation
    if all_costs:
        benchmark_cost_df = pd.concat(all_costs, ignore_index=True)
        benchmark_cost_df = benchmark_cost_df.groupby("Agent", as_index=False).sum(numeric_only=True)
        total_row = benchmark_cost_df.drop(columns=["Agent"]).sum(numeric_only=True)
        total_row["Agent"] = "Total"
        benchmark_cost_df = pd.concat([benchmark_cost_df, pd.DataFrame([total_row])], ignore_index=True)

        print("======================= FINAL BENCHMARK COST SUMMARY =======================")
        print(tabulate(benchmark_cost_df, headers="keys", tablefmt="github"))
        print("============================================================================\n")


# In[7]:


# functions for evaluating cmbagent with agent = 'engineer' (executes code by himself)


# In[8]:


# find result found by cmbagent through execution with regex

def find_result_in_cmbagent_string(cmbagent_answer: dict) -> list[int] | None:
    last_execution_output_message = None

    for message in reversed(cmbagent_answer['chat_history']):
        content = message.get('content', '')
        if "Execution output:" in content:
            last_execution_output_message = content
            break

    if last_execution_output_message:
        match = re.search(r'Execution output:\s*(.*)', last_execution_output_message)
        if match:
            result_str = match.group(1).strip()
            try:
                # Safely parse the string representation of a Python literal (like a list)
                result_list = ast.literal_eval(result_str)
                # Optional: verify it's a list of ints
                if isinstance(result_list, list) and all(isinstance(x, int) for x in result_list):
                    return result_list
                else:
                    print("Parsed result is not a list of ints:", result_list)
                    return None
            except Exception as e:
                print("Error parsing output string:", e)
                return None
        else:
            print("Pattern found but couldn't parse output.")
            return None
    else:
        print("No execution output found in chat history.")
        return None


# In[9]:


# functions for evaluating cmbagent with agent = 'researcher' (execute code locally)


# In[10]:


def extract_code(model_answer: dict) -> str | None:
    content = model_answer["chat_history"][2]["content"]
    matches = re.findall(r"<code>(.*?)</code>", content, re.DOTALL)
    if matches:
        return matches[-1].strip()  # Return the last <code>...</code> block
    print("⚠️ No <code>...</code> block found.")
    return None


# In[11]:


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


# old version:
# def run_python_code_locally_for_one_test_case(code_str: str, input_data: list[int]) -> list[int]:
#     exec_locals = {}

#     # run code 

#     try:
#         exec(code_str, {}, exec_locals)
#     except Exception as e:
#         raise RuntimeError(f"Code execution failed: {e}")

#     # get main function

#     main_func = exec_locals.get("main_function")

#     if not main_func:
#         raise RuntimeError("No function named 'main_function' found in code.")

#     # run example on function

#     try:
#         result = main_func(input_data)
#     except Exception as e:
#         raise RuntimeError(f"Error when calling main_function: {e}")

#     # return result (it is an array)

#     return result


# main benchamrk function for cmbagent

def run_benchmark_on_cmbagent(problems: dict, problem_dir: str, cmbagent_model: str, agent: str) -> dict:

    if agent not in {"engineer", "researcher"}:
        raise ValueError("Agent must be 'engineer' or 'researcher'")

    results_summary = {}
    all_problem_costs = []  # collect all cost DataFrames here
    skipped_problems = []

    total_problems = len(problems)
    c = 0

    for problem_index, (problem_id, problem) in enumerate(problems.items(), start=1):

        print("===============================================================")
        print(f"\t\tEvaluating CMBAgent on problem {problem_index}/{total_problems}: {problem_id}")
        print("===============================================================")

        problem_has_passed = False
        total_time = 0
        error_code = ""
        
        test_cases = load_test_cases_for_one_problem(problem_id, problem_dir)

        if not test_cases:
            skipped_problems.append(problem_id)
            continue

        example_input, example_output = test_cases[0]

        if agent == "engineer":
            prompt = (
                f"Task: {problem['description']}\n"
                f"Example:\n"
                f"Input: {example_input}\n"
                f"Expected Output: {example_output}\n"
                f"Deliver the result strictly as a Python list:\n"
                f"\t- If the result is a single integer n, return it as [n]\n"
                f"\t- If the result is a list, return it as [a, b, c, ...]\n"
                f"Do not include any extra text, explanation, or formatting."
            )

        else:  # researcher
            prompt = (
                f"Task:\n"
                f"Write python code. A function to solve the problem: {problem['description']}\n\n"
                f"Requirements:\n"
                f"- The main function must be named `main_function`, even if helper functions are needed.\n"
                f"- Include all code inside a single <code> ... </code> block, even if you revise it.\n"
                f"- No extra text or explanation, only the code block.\n"
                f"- Execution time must stay under 4 seconds, even for large inputs.\n\n"
                f"Format:\n"
                f"- Input example: {example_input}\n"
                f"- Expected output: {example_output}\n"
                f"- Input and output are python lists. For output:\n"
                f"  - Return [n] for a single integer result.\n"
                f"  - Return [a, b, c, ...] for a list result.\n"
            )

            model_answer = cmbagent.one_shot(
                prompt,
                max_rounds=10,
                agent='researcher',
                researcher_model=cmbagent_model,
            )

            total_time += model_answer['execution_time']

            code_str = extract_code(model_answer)

        correct = 0
        cost_dfs = []

        for i, (input_list, expected_output) in enumerate(test_cases[1:], start=1):

            total_test_cases = len(test_cases) - 1

            if agent == "engineer":

                if i > 1:
                    print("========================================================")
                    print(f"\t\tNEXT TEST CASE ({i}/{total_test_cases}, on problem {problem_index}/{total_problems})")
                    print("========================================================\n")

                test_prompt = (
                    prompt +
                    f"\nFind the answer for the following input:\n{input_list}\nOutput: ?"
                )

                model_answer = cmbagent.one_shot(
                    test_prompt,
                    max_rounds=10,
                    agent='engineer',
                    engineer_model=cmbagent_model,
                )

                parsed_answer = find_result_in_cmbagent_string(model_answer)

                if parsed_answer == expected_output:
                    correct += 1
                total += 1

                cost_df = model_answer["final_context"].data.get("cost_dataframe", pd.DataFrame())
                if not cost_df.empty:
                    cost_df = cost_df[cost_df["Agent"] != "Total"]
                    cost_dfs.append(cost_df)

            else:  # researcher agent

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

                if i == 1:
                    # extract cost data from researcher response once per problem
                    researcher_cost_df = model_answer["final_context"].data.get("cost_dataframe", pd.DataFrame())
                    if not researcher_cost_df.empty:
                        researcher_cost_df = researcher_cost_df[researcher_cost_df["Agent"] != "Total"]
                        cost_dfs.append(researcher_cost_df)

        if total_test_cases == correct:
            problem_has_passed = True

        # Aggregate cost for this problem

        if cost_dfs:
            problem_cost_df = pd.concat(cost_dfs, ignore_index=True)
            problem_cost_df = problem_cost_df.groupby("Agent", as_index=False).sum(numeric_only=True)
            total_row = problem_cost_df.drop(columns=["Agent"]).sum(numeric_only=True)
            total_row["Agent"] = "Total"
            problem_cost_df = pd.concat([problem_cost_df, pd.DataFrame([total_row])], ignore_index=True)
            all_problem_costs.append(problem_cost_df[problem_cost_df["Agent"] != "Total"])
        else:
            problem_cost_df = pd.DataFrame()

        results_summary[problem_id] = {
            "total": total_test_cases,
            "correct": correct,
            "problem_passed": problem_has_passed,
            "problem_time": total_time,
            "error_code": error_code
            #"cost_dataframe": problem_cost_df  # optional per problem cost
        }

        print(f"\n =========== BENCHMARK RESULT FOR CMBAGENT ON PROBLEM {problem_id} ============\n")
        print(f"Total test cases: {total_test_cases}")
        print(f"Correctly guessed test_cases: {correct}")
        print(f"Problem solved: {problem_has_passed}")

        c += 1
        if c == 33:
            break

    print("⚠️ Skipped problems due to non-numeric data (or no test cases):")
    for pid in skipped_problems:
        print(f"- {pid}")

    # Aggregate total cost across all problems
    if all_problem_costs:
        total_cost_df = pd.concat(all_problem_costs, ignore_index=True)
        total_cost_df = total_cost_df.groupby("Agent", as_index=False).sum(numeric_only=True)
        total_row = total_cost_df.drop(columns=["Agent"]).sum(numeric_only=True)
        total_row["Agent"] = "Total"
        total_cost_df = pd.concat([total_cost_df, pd.DataFrame([total_row])], ignore_index=True)

        print("\n=== Total aggregated cost across all problems ===")
        print(tabulate(total_cost_df, headers="keys", tablefmt="github"))
    else:
        print("No cost data available to summarize.")

    return results_summary


# In[13]:


# main wrapper function (this one is called by user and 'does all the work')

def run_benchmark(
    problem_json: str,
    problem_dir: str, 
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

    # Load problems

    problems = load_problems(problem_json)

    # evaluate cmbagent on problems

    if eval_cmbagent: 
        resultscmb = run_benchmark_on_cmbagent(problems, problem_dir, cmbagent_model, "researcher")
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


# In[14]:


# examples


# In[26]:


# # benchmark on 4 extremely easy problems to make sure everything works properly

# info = run_benchmark(
#     problem_json="/mnt/p/stage/cmbagent_benchmark/data/clean/easy_custom_samples.json",
#     problem_dir="/mnt/p/stage/cmbagent_benchmark/data/clean/easy_tests",
#     eval_cmbagent=True,
#     cmbagent_model="gpt-4o-mini"
# )

# print(info)


# # In[28]:


# # test for one long problem (for seeing if compilation takes too long)
# run_benchmark("/mnt/p/stage/cmbagent_benchmark/data/clean/long_pb.json",
#               "/mnt/p/stage/cmbagent_benchmark/data/clean/test_for_long_problem",
#               eval_cmbagent=True,
#               cmbagent_model="gpt-4o-mini",
#               eval_normal_llm=False)


# # In[15]:


# # REAL USACO TEST: 33 PROBLEMS (manually limited)

# run_benchmark("/mnt/p/stage/cmbagent_benchmark/data/clean/usaco_clean_307.json",
#               "/mnt/p/stage/cmbagent_benchmark/data/clean/usaco_tests",
#               eval_cmbagent=True,
#               cmbagent_model="gpt-4o-mini",
#               eval_normal_llm=False)


# # In[ ]:




