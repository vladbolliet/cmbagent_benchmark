
# DEVELOPMENT IN PROGRESS

TODO: add cmbagent (oneshot and planning/control) agents

TODO: add multiprocessing for running multiple agents in parallel

# CMBAgent Oneshot result structure after a call like
```python
task="""
Write a function which takes 2 strings as input and returns the number of characters as output.
"""
result = cmbagent.one_shot(
            task=task,
            max_rounds=5,
            agent='engineer',
            engineer_model='gpt-4.1-2025-04-14'
        )
```

```python
{
    'chat_history': [{
        'content': '\nWrite a function which takes 2 strings as input and returns the number of characters as output.\n',
        'role': 'assistant'
    }, {
        'content': '**Code Explanation:**\n\nThe code defines a function `count_total_characters` that takes two string inputs and returns the total number of characters in both strings combined. The function uses the built-in `len()` function for efficiency. A detailed docstring is provided. An example usage is included, and the result is printed to the console.\n\n**Python Code:**\n\n```python\ndef count_total_characters(str1, str2):\n    """\n    Counts the total number of characters in two input strings.\n\n    Parameters\n    ----------\n    str1 : str\n        The first input string.\n    str2 : str\n        The second input string.\n\n    Returns\n    -------\n    int\n        The total number of characters in both input strings.\n    """\n    return len(str1) + len(str2)\n\n# Example usage\nstring1 = "hello"\nstring2 = "world"\ntotal_characters = count_total_characters(string1, string2)\nprint("Total number of characters in the two strings: " + str(total_characters))\n```',
        'name': 'engineer',
        'role': 'user'
    }, {
        'content': '\nThe executed code was:\n\n```python\n# filename: codebase/count_characters.py\ndef count_total_characters(str1, str2):\n    """\n    Counts the total number of characters in two input strings.\n\n    Parameters\n    ----------\n    str1 : str\n        The first input string.\n    str2 : str\n        The second input string.\n\n    Returns\n    -------\n    int\n        The total number of characters in both input strings.\n    """\n    return len(str1) + len(str2)\n\n# Example usage\nstring1 = "hello"\nstring2 = "world"\ntotal_characters = count_total_characters(string1, string2)\nprint("Total number of characters in the two strings: " + str(total_characters))\n```\n\n================================================    \n\nThe output of the executed code was:\n\nExecution results:\n\nExecution output: \nTotal number of characters in the two strings: 10\n\n\n================================================    \n                        ',
        'name': 'engineer_nest',
        'role': 'user'
    }, {
        'content': 'None',
        'tool_calls': [{
            'id': 'call_lJwUdp4uTDtrkKYjbeIC8yJg',
            'function': {
                'arguments': '{"next_agent_suggestion": "control", "execution_status": "success", "fix_suggestion": null}',
                'name': 'post_execution_transfer'
            },
            'type': 'function'
        }],
        'name': 'executor_response_formatter',
        'role': 'assistant'
    }, {
        'content': 'Execution status: success. Transfer to control.\n\nxxxxxxxxxxxxxxxxxxxxxxxxxx\n\nWorkflow status:\n\nPlan step number: 1\n\nAgent for sub-task (might be different from the next agent suggestion for debugging): engineer\n\nCurrent status (before execution): In progress\n\nxxxxxxxxxxxxxxxxxxxxxxxxxx\n\n',
        'tool_responses': [{
            'tool_call_id': 'call_lJwUdp4uTDtrkKYjbeIC8yJg',
            'role': 'tool',
            'content': 'Execution status: success. Transfer to control.\n\nxxxxxxxxxxxxxxxxxxxxxxxxxx\n\nWorkflow status:\n\nPlan step number: 1\n\nAgent for sub-task (might be different from the next agent suggestion for debugging): engineer\n\nCurrent status (before execution): In progress\n\nxxxxxxxxxxxxxxxxxxxxxxxxxx\n\n'
        }],
        'name': '_Group_Tool_Executor',
        'role': 'tool'
    }],
    'final_context': ContextVariables(data = {
        'plans': [],
        'reviews': [],
        'proposed_plan': None,
        'recommendations': None,
        'feedback_left': 0,
        'number_of_steps_in_plan': 1,
        'maximum_number_of_steps_in_plan': 1,
        'final_plan': 'Step 1: solve the main task.',
        'current_plan_step_number': 1,
        'current_sub_task': 'solve the main task.',
        'agent_for_sub_task': 'engineer',
        'current_status': 'In progress',
        'current_instructions': 'solve the main task.',
        'main_task': '\nWrite a function which takes 2 strings as input and returns the number of characters as output.\n',
        'improved_main_task': '\nWrite a function which takes 2 strings as input and returns the number of characters as output.\n',
        'database_path': 'data/',
        'codebase_path': 'codebase/',
        'current_codebase': None,
        'displayed_images': [],
        'transfer_to_engineer': False,
        'transfer_to_researcher': False,
        'transfer_to_camb_agent': False,
        'transfer_to_classy_agent': False,
        'transfer_to_cobaya_agent': False,
        'transfer_to_perplexity': False,
        'transfer_to_camb_context': False,
        'transfer_to_classy_context': False,
        'planner_append_instructions': None,
        'plan_reviewer_append_instructions': None,
        'engineer_append_instructions': '',
        'researcher_append_instructions': '',
        'previous_steps_execution_summary': '\n',
        'hardware_constraints': None,
        'AAS_keywords_string': None,
        'text_input_for_AAS_keyword_finder': None,
        'N_AAS_keywords': 5,
        'perplexity_query': None,
        'perplexity_response': None,
        'perplexity_citations': None,
        'n_attempts': 0,
        'max_n_attempts': 3,
        'camb_context': None,
        'classy_context': None,
        'researcher_filename': 'provide a suitable filename given the nature of the notes. Prefer markdown extension unless otherwise instructed.',
        'perplexity_append_instructions': '',
        'idea_maker_append_instructions': '',
        'idea_hater_append_instructions': '',
        'work_dir': '/mnt/p/stage/cmbagent_benchmark/cmbagent_output',
        'cost_dataframe': Agent Cost($) Prompt Tokens Completion Tokens Total Tokens Model
        0 engineer 0.004890 1601.0 211.0 1812.0 gpt - 4.1 - 2025 - 04 - 14
        1 engineer response formatter 0.003698 974.0 597.0 1571.0 o3 - mini - 2025 - 01 - 31
        2 executor response formatter 0.001219 704.0 101.0 805.0 o3 - mini - 2025 - 01 - 31
        Total Total 0.009807 3279.0 909.0 4188.0 NaN,
        'cost_report_path': '/mnt/p/stage/cmbagent_benchmark/cmbagent_output/cost/cost_report_20250804_033159.json'
    }),
    'engineer': < cmbagent.agents.engineer.engineer.EngineerAgent object at 0x7696f4f71ac0 > ,
    'engineer_response_formatter': < cmbagent.agents.engineer_response_formatter.engineer_response_formatter.EngineerResponseFormatterAgent object at 0x7696d5249a90 > ,
    'researcher': < cmbagent.agents.researcher.researcher.ResearcherAgent object at 0x7696d1d489e0 > ,
    'researcher_response_formatter': < cmbagent.agents.researcher_response_formatter.researcher_response_formatter.ResearcherResponseFormatterAgent object at 0x7696f4bad940 > ,
    'initialization_time': 3.6174259185791016,
    'execution_time': 16.52610945701599
}

# Keeping track of changes while implementing cmbagent oneshot

Added this to model_config.yaml. Everything after 'name:' is considered an agent name, in yaml file
```yaml
cmbagent:
  - name: oneshot
  - name: planning_and_control
``` 

# EXAMPLE USE OF PLANNING_AND_CONTROL
```python
task="""
Write a function which takes 2 strings as input and returns the number of characters as output.
"""
model_answer = cmbagent.planning_and_control_context_carryover(
                              task=task,
                              max_rounds_planning = 5,
                              max_rounds_control = 5,
                              max_plan_steps=5,
                              n_plan_reviews = 2,
                              plan_instructions="Engineer agent should generate Python code for the problem, researcher agent should validate correctness and edge cases.",
                              engineer_instructions="Write efficient, clean Python code.",
                              researcher_instructions="Check code for correctness, edge cases, and performance.",
                              hardware_constraints="Code should run in <10 seconds and use only standard Python libraries.",
                              max_n_attempts = 2,
                              default_llm_model = "gpt-4.1-2025-04-14",
                              planner_model = "gpt-4.1-2025-04-14",
                              plan_reviewer_model = "claude-3-7-sonnet-20250219",
                              engineer_model = "gemini-2.5-pro",
                              researcher_model = "gpt-4.1-2025-04-14"
        )     
```
RESULT OF RUNNING THAT:
```python

```
























CMBAgent Benchmark

Overview of the project and its components

Structure of the project:

- `new_code_v4/`: Contains the latest version of the codebase. (will be changed to root directory when the project is finalized)
- `model_config.yaml`: Configuration file for the models used in the benchmark.
- `create_benchmark.sh`: Script to create a benchmark configuration.
- `run_benchmark.py`: Script to run the benchmark with the specified configuration.
- `python scripts`: Various Python scripts that implement the benchmark logic
- `README.md`: This file, providing an overview of the project and instructions for use.
- `benchmark_output/`: Directory where benchmark results and individual configs will be saved.

Starting file(s):

- `model_config.yaml`: Configuration file for the models used in the benchmark (contains models that can be used in the benchmark).
- `create_benchmark.sh`: Script to create a benchmark configuration. (for selecting agents, this file accepts only agents present in `model_config.yaml`). Also, everything this .sh does is create a benchmark configuration yaml file, saved in its own benchmark directory, which contains data about where our problems are located, how we want to select the problems and which agents to use. The format of this yaml file is as follows:

```yaml
json_file_path: <path-to-json-file>
test_cases_folder_path: <path-to-test-cases-folder>
problem:
    selection_type: "<by_level | random | by_id>"

    # If selection_type is "by_level":
    bronze: <int>
    silver: <int>
    gold: <int>
    platinum: <int>

    # If selection_type is "random":
    count: <int>
    # Only present if user chooses to avoid levels within "random":
    avoid_levels: [bronze,silver,gold,platinum]  # comma-separated, any subset

    # If selection_type is "by_id":
    list: [id1,id2,id3,...]  # comma-separated problem IDs

# Only present if user chooses to specify agent names:
agents: [agent1,agent2,...]  # comma-separated, must match names in model_config.yaml
```

This yaml file will be used by the python scripts for running the benchmark


