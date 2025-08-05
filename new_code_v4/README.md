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
# RESULT OF RUNNING THAT:

```python
{
    'chat_history': [{
        'content': '\nWrite a function which takes 2 strings as input and returns the number of characters as output.\n',
        'role': 'assistant'
    }, {
        'content': 'None',
        'tool_calls': [{
            'id': 'call_HjHaPs9kZGE1fxAXjricPN6X',
            'function': {
                'arguments': '{}',
                'name': 'record_status_starter'
            },
            'type': 'function'
        }],
        'name': 'control_starter',
        'role': 'assistant'
    }, {
        'content': '\n**Step number:** 2 out of 2.\n \n**Sub-task:** Analyze and discuss the function’s behavior, edge cases, and computational characteristics.\n \n**Agent in charge of sub-task:** `researcher`\n \n**Instructions:**\n \n- Explain how the function works and what its output represents.\n- Discuss how the function handles edge cases, such as empty strings, None values, or non-string inputs.\n- Analyze the performance characteristics and computational complexity of the string length calculation.\n- Mention potential applications or scenarios where such a function might be useful.\n- Note any limitations or considerations regarding the function’s use.\n \n**Status:** in progress ⏳\n',
        'tool_responses': [{
            'tool_call_id': 'call_HjHaPs9kZGE1fxAXjricPN6X',
            'role': 'tool',
            'content': '\n**Step number:** 2 out of 2.\n \n**Sub-task:** Analyze and discuss the function’s behavior, edge cases, and computational characteristics.\n \n**Agent in charge of sub-task:** `researcher`\n \n**Instructions:**\n \n- Explain how the function works and what its output represents.\n- Discuss how the function handles edge cases, such as empty strings, None values, or non-string inputs.\n- Analyze the performance characteristics and computational complexity of the string length calculation.\n- Mention potential applications or scenarios where such a function might be useful.\n- Note any limitations or considerations regarding the function’s use.\n \n**Status:** in progress ⏳\n'
        }],
        'name': '_Group_Tool_Executor',
        'role': 'tool'
    }, {
        'content': '# Analysis and Discussion of the String Character Counting Function\n\n## Function Overview\n\nThe implemented function, `get_total_character_count(str1, str2)`, accepts two arguments and returns the total number of characters contained in both strings. The function first validates that both inputs are of type `str`. If either input is not a string, it raises a `TypeError`. If both inputs are valid, it computes the sum of their lengths using the built-in `len()` function and returns the result.\n\n## Output Interpretation\n\nThe output of the function is an integer representing the combined number of characters in the two input strings. For example, given the inputs `"hello"` and `"world"`, the function returns `10`, as each string contains five characters.\n\n## Handling of Edge Cases\n\n### Empty Strings\n\n- If either or both input strings are empty (`""`), the function correctly returns the length of the non-empty string or zero if both are empty.\n- Example: `get_total_character_count("", "")` returns `0`.\n\n### Non-String Inputs\n\n- The function explicitly checks the type of both inputs.\n- If either input is not a string (e.g., integer, list, `None`), a `TypeError` is raised with a clear error message.\n- This behavior is robust and prevents silent failures or incorrect results.\n\n### Special Characters and Unicode\n\n- The function counts all characters, including whitespace, punctuation, special symbols, and Unicode characters, as individual characters.\n- Example: `get_total_character_count("!@#", "你好")` returns `5` (three ASCII symbols and two Chinese characters).\n\n### Long Strings\n\n- The function handles long strings efficiently, as the `len()` operation in Python is optimized for string objects.\n\n## Computational Complexity\n\n- The time complexity of the function is O(1) for each call to `len()` because Python strings store their length as an internal attribute.\n- The overall time complexity is O(1), as the function performs a constant number of operations regardless of the string lengths.\n- The space complexity is also O(1), as no additional data structures are created.\n\n## Potential Applications\n\n- **Text Analytics:** Quickly determining the combined length of two text fields (e.g., first and last names, title and subtitle).\n- **Input Validation:** Enforcing character limits across multiple input fields in forms or user interfaces.\n- **Data Processing:** Summing the lengths of string pairs in batch processing or data cleaning tasks.\n- **Educational Tools:** Demonstrating string operations and type checking in programming education.\n\n## Limitations and Considerations\n\n- **Strict Type Enforcement:** The function does not attempt to coerce non-string inputs to strings (e.g., via `str()`), which may be desirable in some flexible applications but ensures type safety and predictability.\n- **No Support for Iterable Concatenation:** The function only accepts two arguments; it does not handle lists or tuples of strings.\n- **No Handling of Encoding Issues:** The function assumes that the input strings are properly encoded and do not contain invalid byte sequences.\n\n## Summary\n\nThe function is robust, efficient, and well-suited for scenarios requiring the combined character count of two strings. Its strict input validation ensures reliability, and its computational characteristics make it suitable for use in performance-sensitive contexts. The function\'s design is clear and its behavior is predictable across a wide range of input scenarios.',
        'name': 'researcher',
        'role': 'user'
    }, {
        'content': '**Markdown:**\n\n```markdown\n<!-- filename: string_character_count_analysis.md -->\n# Analysis and Discussion of the String Character Counting Function\n\n## Function Overview\n\nThe implemented function, `get_total_character_count(str1, str2)`, accepts two arguments and returns the total number of characters contained in both strings. The function first validates that both inputs are of type `str`. If either input is not a string, it raises a `TypeError`. If both inputs are valid, it computes the sum of their lengths using the built-in `len()` function and returns the result.\n\n## Output Interpretation\n\nThe output of the function is an integer representing the combined number of characters in the two input strings. For example, given the inputs "hello" and "world", the function returns `10`, as each string contains five characters.\n\n## Handling of Edge Cases\n\n### Empty Strings\n\n- If either or both input strings are empty (""), the function correctly returns the length of the non-empty string or zero if both are empty.\n- Example: `get_total_character_count("", "")` returns `0`.\n\n### Non-String Inputs\n\n- The function explicitly checks the type of both inputs.\n- If either input is not a string (e.g., integer, list, `None`), a `TypeError` is raised with a clear error message.\n- This behavior is robust and prevents silent failures or incorrect results.\n\n### Special Characters and Unicode\n\n- The function counts all characters, including whitespace, punctuation, special symbols, and Unicode characters, as individual characters.\n- Example: `get_total_character_count("!@#", "你好")` returns `5` (three ASCII symbols and two Chinese characters).\n\n### Long Strings\n\n- The function handles long strings efficiently, as the `len()` operation in Python is optimized for string objects.\n\n## Computational Complexity\n\n- The time complexity of the function is O(1) for each call to `len()` because Python strings store their length as an internal attribute.\n- The overall time complexity is O(1), as the function performs a constant number of operations regardless of the string lengths.\n- The space complexity is also O(1), as no additional data structures are created.\n\n## Potential Applications\n\n- **Text Analytics:** Quickly determining the combined length of two text fields (e.g., first and last names, title and subtitle).\n- **Input Validation:** Enforcing character limits across multiple input fields in forms or user interfaces.\n- **Data Processing:** Summing the lengths of string pairs in batch processing or data cleaning tasks.\n- **Educational Tools:** Demonstrating string operations and type checking in programming education.\n\n## Limitations and Considerations\n\n- **Strict Type Enforcement:** The function does not attempt to coerce non-string inputs to strings (e.g., via `str()`), which may be desirable in some flexible applications but ensures type safety and predictability.\n- **No Support for Iterable Concatenation:** The function only accepts two arguments; it does not handle lists or tuples of strings.\n- **No Handling of Encoding Issues:** The function assumes that the input strings are properly encoded and do not contain invalid byte sequences.\n\n## Summary\n\nThe function is robust, efficient, and well-suited for scenarios requiring the combined character count of two strings. Its strict input validation ensures reliability, and its computational characteristics make it suitable for use in performance-sensitive contexts. The function\'s design is clear and its behavior is predictable across a wide range of input scenarios.\n```',
        'name': 'researcher_response_formatter',
        'role': 'user'
    }, {
        'content': 'Execution results:\n\nExecution output: Content saved to /mnt/p/stage/cmbagent_benchmark/cmbagent_output/control/string_character_count_analysis.md\n',
        'name': 'researcher_executor',
        'role': 'user'
    }, {
        'content': 'None',
        'tool_calls': [{
            'id': 'call_QNlUIc3LlPn9JUyjLkvYIBKF',
            'function': {
                'arguments': '{"current_status":"completed","current_plan_step_number":2,"current_sub_task":"Analyze and discuss the function’s behavior, edge cases, and computational characteristics.","current_instructions":"- Explain how the function works and what its output represents.\\n- Discuss how the function handles edge cases, such as empty strings, None values, or non-string inputs.\\n- Analyze the performance characteristics and computational complexity of the string length calculation.\\n- Mention potential applications or scenarios where such a function might be useful.\\n- Note any limitations or considerations regarding the function’s use.","agent_for_sub_task":"researcher"}',
                'name': 'record_status'
            },
            'type': 'function'
        }],
        'name': 'control',
        'role': 'assistant'
    }, {
        'content': '\n**Step number:** 2 out of 2.\n \n**Sub-task:** Analyze and discuss the function’s behavior, edge cases, and computational characteristics.\n \n**Agent in charge of sub-task:** `researcher`\n \n**Instructions:**\n \n- Explain how the function works and what its output represents.\n- Discuss how the function handles edge cases, such as empty strings, None values, or non-string inputs.\n- Analyze the performance characteristics and computational complexity of the string length calculation.\n- Mention potential applications or scenarios where such a function might be useful.\n- Note any limitations or considerations regarding the function’s use.\n \n**Status:** completed ✅\n        ',
        'tool_responses': [{
            'tool_call_id': 'call_QNlUIc3LlPn9JUyjLkvYIBKF',
            'role': 'tool',
            'content': '\n**Step number:** 2 out of 2.\n \n**Sub-task:** Analyze and discuss the function’s behavior, edge cases, and computational characteristics.\n \n**Agent in charge of sub-task:** `researcher`\n \n**Instructions:**\n \n- Explain how the function works and what its output represents.\n- Discuss how the function handles edge cases, such as empty strings, None values, or non-string inputs.\n- Analyze the performance characteristics and computational complexity of the string length calculation.\n- Mention potential applications or scenarios where such a function might be useful.\n- Note any limitations or considerations regarding the function’s use.\n \n**Status:** completed ✅\n        '
        }],
        'name': '_Group_Tool_Executor',
        'role': 'tool'
    }, {
        'content': 'None',
        'tool_calls': [{
            'id': 'call_5dmfGMVsktBJHhG1fsMdCqRz',
            'function': {
                'arguments': '{}',
                'name': 'terminate_session'
            },
            'type': 'function'
        }],
        'name': 'terminator',
        'role': 'assistant'
    }, {
        'content': 'Session terminated.',
        'tool_responses': [{
            'tool_call_id': 'call_5dmfGMVsktBJHhG1fsMdCqRz',
            'role': 'tool',
            'content': 'Session terminated.'
        }],
        'name': '_Group_Tool_Executor',
        'role': 'tool'
    }],
    'final_context': ContextVariables(data = {
        'plans': ["- Step 1:\n\t* sub-task: Implement a function that takes two strings as input and returns the total number of characters.\n\t* agent in charge: engineer\n\n\t* instructions:\n\t\t- Write a function that accepts two string arguments.\n\t\t- Calculate the total number of characters by summing the lengths of both strings.\n\t\t- Return the computed total as the output.\n\n- Step 2:\n\t* sub-task: Discuss the function's behavior and possible use cases.\n\t* agent in charge: researcher\n\n\t* instructions:\n\t\t- Explain how the function works and what its output represents.\n\t\t- Discuss potential applications or scenarios where such a function might be useful.\n\t\t- Mention any limitations or considerations regarding the function's use.\n", '- Step 1:\n\t* sub-task: Implement a function that takes two strings as input and returns the total number of characters, with robust validation and documentation.\n\t* agent in charge: engineer\n\n\t* instructions:\n\t\t- Write a function that accepts two arguments and validates that both are strings; raise an appropriate error if not.\n\t\t- Calculate the total number of characters by summing the lengths of both strings.\n\t\t- Add a comprehensive docstring explaining the parameters, return value, error handling, and provide usage examples.\n\t\t- Develop and run test cases to verify the function works correctly with various string inputs, including empty strings, single characters, long strings, and strings with special characters.\n\t\t- Ensure the function handles edge cases and invalid input gracefully.\n\n- Step 2:\n\t* sub-task: Analyze and discuss the function’s behavior, edge cases, and computational characteristics.\n\t* agent in charge: researcher\n\n\t* instructions:\n\t\t- Explain how the function works and what its output represents.\n\t\t- Discuss how the function handles edge cases, such as empty strings, None values, or non-string inputs.\n\t\t- Analyze the performance characteristics and computational complexity of the string length calculation.\n\t\t- Mention potential applications or scenarios where such a function might be useful.\n\t\t- Note any limitations or considerations regarding the function’s use.\n'],
        'reviews': ['Recommendations:\n\n1. Add testing and validation instructions to Step 1 for the engineer to include test cases that verify the function works correctly with various string inputs (empty strings, single characters, long strings, strings with special characters).\n\n2. Expand Step 1 instructions to include proper function documentation with docstrings explaining parameters, return value, and providing usage examples.\n\n3. Enhance Step 2 instructions for the researcher to include discussion of edge cases and how the function handles them (such as empty strings, None values, or non-string inputs).\n\n4. Modify Step 1 to include error handling considerations, instructing the engineer to implement input validation to ensure both parameters are strings.\n\n5. Refine Step 2 instructions to have the researcher discuss performance characteristics and computational complexity of the string length calculation approach.'],
        'proposed_plan': '- Step 1:\n\t* sub-task: Implement a function that takes two strings as input and returns the total number of characters, with robust validation and documentation.\n\t* agent in charge: engineer\n\n\t* instructions:\n\t\t- Write a function that accepts two arguments and validates that both are strings; raise an appropriate error if not.\n\t\t- Calculate the total number of characters by summing the lengths of both strings.\n\t\t- Add a comprehensive docstring explaining the parameters, return value, error handling, and provide usage examples.\n\t\t- Develop and run test cases to verify the function works correctly with various string inputs, including empty strings, single characters, long strings, and strings with special characters.\n\t\t- Ensure the function handles edge cases and invalid input gracefully.\n\n- Step 2:\n\t* sub-task: Analyze and discuss the function’s behavior, edge cases, and computational characteristics.\n\t* agent in charge: researcher\n\n\t* instructions:\n\t\t- Explain how the function works and what its output represents.\n\t\t- Discuss how the function handles edge cases, such as empty strings, None values, or non-string inputs.\n\t\t- Analyze the performance characteristics and computational complexity of the string length calculation.\n\t\t- Mention potential applications or scenarios where such a function might be useful.\n\t\t- Note any limitations or considerations regarding the function’s use.\n',
        'recommendations': 'Recommendations:\n\n1. Add testing and validation instructions to Step 1 for the engineer to include test cases that verify the function works correctly with various string inputs (empty strings, single characters, long strings, strings with special characters).\n\n2. Expand Step 1 instructions to include proper function documentation with docstrings explaining parameters, return value, and providing usage examples.\n\n3. Enhance Step 2 instructions for the researcher to include discussion of edge cases and how the function handles them (such as empty strings, None values, or non-string inputs).\n\n4. Modify Step 1 to include error handling considerations, instructing the engineer to implement input validation to ensure both parameters are strings.\n\n5. Refine Step 2 instructions to have the researcher discuss performance characteristics and computational complexity of the string length calculation approach.',
        'feedback_left': 0,
        'number_of_steps_in_plan': 2,
        'maximum_number_of_steps_in_plan': 2,
        'final_plan': '- Step 1:\n\t* sub-task: Implement a function that takes two strings as input and returns the total number of characters, with robust validation and documentation.\n\t* agent in charge: engineer\n\n\t* instructions:\n\t\t- Write a function that accepts two arguments and validates that both are strings; raise an appropriate error if not.\n\t\t- Calculate the total number of characters by summing the lengths of both strings.\n\t\t- Add a comprehensive docstring explaining the parameters, return value, error handling, and provide usage examples.\n\t\t- Develop and run test cases to verify the function works correctly with various string inputs, including empty strings, single characters, long strings, and strings with special characters.\n\t\t- Ensure the function handles edge cases and invalid input gracefully.\n\n- Step 2:\n\t* sub-task: Analyze and discuss the function’s behavior, edge cases, and computational characteristics.\n\t* agent in charge: researcher\n\n\t* instructions:\n\t\t- Explain how the function works and what its output represents.\n\t\t- Discuss how the function handles edge cases, such as empty strings, None values, or non-string inputs.\n\t\t- Analyze the performance characteristics and computational complexity of the string length calculation.\n\t\t- Mention potential applications or scenarios where such a function might be useful.\n\t\t- Note any limitations or considerations regarding the function’s use.\n',
        'current_plan_step_number': 2,
        'current_sub_task': 'Analyze and discuss the function’s behavior, edge cases, and computational characteristics.',
        'agent_for_sub_task': 'researcher',
        'current_status': 'completed',
        'current_instructions': '- Explain how the function works and what its output represents.\n- Discuss how the function handles edge cases, such as empty strings, None values, or non-string inputs.\n- Analyze the performance characteristics and computational complexity of the string length calculation.\n- Mention potential applications or scenarios where such a function might be useful.\n- Note any limitations or considerations regarding the function’s use.',
        'main_task': '\nWrite a function which takes 2 strings as input and returns the number of characters as output.\n',
        'improved_main_task': '\nWrite a function which takes 2 strings as input and returns the number of characters as output.\n',
        'database_path': 'data/',
        'codebase_path': 'codebase/',
        'current_codebase': '-----------\nFilename: character_count.py\nFile path: codebase/character_count.py\n\nAvailable functions:\nfunction name: get_total_character_count\n````\nCalculates the total number of characters in two strings.\n\nThis function takes two strings as input, validates that both inputs are\nof type string, and then returns the sum of their lengths.\n\nParameters:\nstr1 (str): The first string.\nstr2 (str): The second string.\n\nReturns:\nint: The total number of characters in both strings combined.\n\nRaises:\nTypeError: If either of the inputs is not a string.\n\nExamples:\n>>> get_total_character_count("hello", "world")\n10\n>>> get_total_character_count("", "test")\n4\n>>> get_total_character_count("!@#$", "123")\n7\n````\n\n',
        'displayed_images': [],
        'transfer_to_engineer': False,
        'transfer_to_researcher': False,
        'transfer_to_camb_agent': False,
        'transfer_to_classy_agent': False,
        'transfer_to_cobaya_agent': False,
        'transfer_to_perplexity': False,
        'transfer_to_camb_context': False,
        'transfer_to_classy_context': False,
        'planner_append_instructions': '\nUse engineer for whole analysis, and researcher at the very end. Plan must have 2 steps.\nThe plan must strictly involve only the following agents: engineer, researcher\n\n**AGENT ROLES**\nHere are the descriptions of the agents that are needed to carry out the plan:\n- researcher: To generate the discussion and interpretation of the results, or background information on the topic. This agent does not run code or see plots. It only discusses results or background information on the topic.\n- engineer: To generate the results and do the computations, plots and key statistics via code pipelines.\n\n\nYou must not invoke any other agent than the ones listed above.\n',
        'plan_reviewer_append_instructions': '\nUse engineer for whole analysis, and researcher at the very end. Plan must have 2 steps.\nThe plan must strictly involve only the following agents: engineer, researcher\n\n**AGENT ROLES**\nHere are the descriptions of the agents that are needed to carry out the plan:\n- researcher: To generate the discussion and interpretation of the results, or background information on the topic. This agent does not run code or see plots. It only discusses results or background information on the topic.\n- engineer: To generate the results and do the computations, plots and key statistics via code pipelines.\n\n\nYou must not invoke any other agent than the ones listed above.\n',
        'engineer_append_instructions': '',
        'researcher_append_instructions': '',
        'previous_steps_execution_summary': '### Step 1\nThe executed code was:\n\n```python\n# filename: codebase/character_count.py\nimport sys\n\ndef get_total_character_count(str1, str2):\n    """\n    Calculates the total number of characters in two strings.\n\n    This function takes two strings as input, validates that both inputs are\n    of type string, and then returns the sum of their lengths.\n\n    Parameters:\n    str1 (str): The first string.\n    str2 (str): The second string.\n\n    Returns:\n    int: The total number of characters in both strings combined.\n\n    Raises:\n    TypeError: If either of the inputs is not a string.\n\n    Examples:\n    >>> get_total_character_count("hello", "world")\n    10\n    >>> get_total_character_count("", "test")\n    4\n    >>> get_total_character_count("!@#$", "123")\n    7\n    """\n    if not isinstance(str1, str) or not isinstance(str2, str):\n        raise TypeError("Both inputs must be strings.")\n    return len(str1) + len(str2)\n\nif __name__ == \'__main__\':\n    # Test cases for the function\n    test_cases = [\n        # Valid inputs\n        {"name": "Two standard strings", "input": ("hello", "world"), "expected": 10, "raises": None},\n        {"name": "First string empty", "input": ("", "world"), "expected": 5, "raises": None},\n        {"name": "Second string empty", "input": ("hello", ""), "expected": 5, "raises": None},\n        {"name": "Both strings empty", "input": ("", ""), "expected": 0, "raises": None},\n        {"name": "Single character strings", "input": ("a", "b"), "expected": 2, "raises": None},\n        {"name": "Long strings", "input": ("a" * 100, "b" * 200), "expected": 300, "raises": None},\n        {"name": "Strings with special characters", "input": ("!@#$%^", "&*()"), "expected": 10, "raises": None},\n        {"name": "Strings with numbers and spaces", "input": ("123 456", " 789 "), "expected": 12, "raises": None},\n\n        # Invalid inputs\n        {"name": "First input is integer", "input": (123, "world"), "expected": None, "raises": TypeError},\n        {"name": "Second input is integer", "input": ("hello", 456), "expected": None, "raises": TypeError},\n        {"name": "First input is None", "input": (None, "world"), "expected": None, "raises": TypeError},\n        {"name": "Second input is None", "input": ("hello", None), "expected": None, "raises": TypeError},\n        {"name": "First input is list", "input": (["a"], "world"), "expected": None, "raises": TypeError},\n        {"name": "Second input is list", "input": ("hello", ["b"]), "expected": None, "raises": TypeError},\n    ]\n\n    all_tests_passed = True\n    print("Running test cases for get_total_character_count...")\n\n    for i, test in enumerate(test_cases):\n        test_passed = False\n        try:\n            result = get_total_character_count(test["input"][0], test["input"][1])\n            if test["raises"] is None:\n                if result == test["expected"]:\n                    print("Test " + str(i + 1) + " (\'" + test["name"] + "\'): PASSED")\n                    test_passed = True\n                else:\n                    print("Test " + str(i + 1) + " (\'" + test["name"] + "\'): FAILED - Expected " + str(test["expected"]) + ", got " + str(result))\n            else:\n                print("Test " + str(i + 1) + " (\'" + test["name"] + "\'): FAILED - Expected exception " + str(test["raises"]) + ", but none was raised.")\n\n        except Exception as e:\n            if test["raises"] is not None and isinstance(e, test["raises"]):\n                print("Test " + str(i + 1) + " (\'" + test["name"] + "\'): PASSED - Correctly raised " + str(type(e).__name__))\n                test_passed = True\n            else:\n                print("Test " + str(i + 1) + " (\'" + test["name"] + "\'): FAILED - Unexpected exception " + str(type(e).__name__) + ": " + str(e))\n        \n        if not test_passed:\n            all_tests_passed = False\n\n    print("\\n" + "="*30)\n    if all_tests_passed:\n        print("All tests passed successfully!")\n    else:\n        print("Some tests failed.")\n    print("="*30 + "\\n")\n\n    # Example usage demonstration\n    print("Demonstrating function usage:")\n    str_a = "Python"\n    str_b = "is fun!"\n    total_chars = get_total_character_count(str_a, str_b)\n    print("The total number of characters in \'" + str_a + "\' and \'" + str_b + "\' is: " + str(total_chars))\n```\n\n================================================    \n\nThe output of the executed code was:\n\nExecution results:\n\nExecution output: \nRunning test cases for get_total_character_count...\nTest 1 (\'Two standard strings\'): PASSED\nTest 2 (\'First string empty\'): PASSED\nTest 3 (\'Second string empty\'): PASSED\nTest 4 (\'Both strings empty\'): PASSED\nTest 5 (\'Single character strings\'): PASSED\nTest 6 (\'Long strings\'): PASSED\nTest 7 (\'Strings with special characters\'): PASSED\nTest 8 (\'Strings with numbers and spaces\'): PASSED\nTest 9 (\'First input is integer\'): PASSED - Correctly raised TypeError\nTest 10 (\'Second input is integer\'): PASSED - Correctly raised TypeError\nTest 11 (\'First input is None\'): PASSED - Correctly raised TypeError\nTest 12 (\'Second input is None\'): PASSED - Correctly raised TypeError\nTest 13 (\'First input is list\'): PASSED - Correctly raised TypeError\nTest 14 (\'Second input is list\'): PASSED - Correctly raised TypeError\n\n==============================\nAll tests passed successfully!\n==============================\n\nDemonstrating function usage:\nThe total number of characters in \'Python\' and \'is fun!\' is: 13\n\n\n================================================\n\n### Step 2\n**Markdown:**\n\n```markdown\n<!-- filename: string_character_count_analysis.md -->\n# Analysis and Discussion of the String Character Counting Function\n\n## Function Overview\n\nThe implemented function, `get_total_character_count(str1, str2)`, accepts two arguments and returns the total number of characters contained in both strings. The function first validates that both inputs are of type `str`. If either input is not a string, it raises a `TypeError`. If both inputs are valid, it computes the sum of their lengths using the built-in `len()` function and returns the result.\n\n## Output Interpretation\n\nThe output of the function is an integer representing the combined number of characters in the two input strings. For example, given the inputs "hello" and "world", the function returns `10`, as each string contains five characters.\n\n## Handling of Edge Cases\n\n### Empty Strings\n\n- If either or both input strings are empty (""), the function correctly returns the length of the non-empty string or zero if both are empty.\n- Example: `get_total_character_count("", "")` returns `0`.\n\n### Non-String Inputs\n\n- The function explicitly checks the type of both inputs.\n- If either input is not a string (e.g., integer, list, `None`), a `TypeError` is raised with a clear error message.\n- This behavior is robust and prevents silent failures or incorrect results.\n\n### Special Characters and Unicode\n\n- The function counts all characters, including whitespace, punctuation, special symbols, and Unicode characters, as individual characters.\n- Example: `get_total_character_count("!@#", "你好")` returns `5` (three ASCII symbols and two Chinese characters).\n\n### Long Strings\n\n- The function handles long strings efficiently, as the `len()` operation in Python is optimized for string objects.\n\n## Computational Complexity\n\n- The time complexity of the function is O(1) for each call to `len()` because Python strings store their length as an internal attribute.\n- The overall time complexity is O(1), as the function performs a constant number of operations regardless of the string lengths.\n- The space complexity is also O(1), as no additional data structures are created.\n\n## Potential Applications\n\n- **Text Analytics:** Quickly determining the combined length of two text fields (e.g., first and last names, title and subtitle).\n- **Input Validation:** Enforcing character limits across multiple input fields in forms or user interfaces.\n- **Data Processing:** Summing the lengths of string pairs in batch processing or data cleaning tasks.\n- **Educational Tools:** Demonstrating string operations and type checking in programming education.\n\n## Limitations and Considerations\n\n- **Strict Type Enforcement:** The function does not attempt to coerce non-string inputs to strings (e.g., via `str()`), which may be desirable in some flexible applications but ensures type safety and predictability.\n- **No Support for Iterable Concatenation:** The function only accepts two arguments; it does not handle lists or tuples of strings.\n- **No Handling of Encoding Issues:** The function assumes that the input strings are properly encoded and do not contain invalid byte sequences.\n\n## Summary\n\nThe function is robust, efficient, and well-suited for scenarios requiring the combined character count of two strings. Its strict input validation ensures reliability, and its computational characteristics make it suitable for use in performance-sensitive contexts. The function\'s design is clear and its behavior is predictable across a wide range of input scenarios.\n```',
        'hardware_constraints': '',
        'AAS_keywords_string': None,
        'text_input_for_AAS_keyword_finder': None,
        'N_AAS_keywords': 5,
        'perplexity_query': None,
        'perplexity_response': None,
        'perplexity_citations': None,
        'n_attempts': 0,
        'max_n_attempts': 2,
        'camb_context': None,
        'classy_context': None,
        'researcher_filename': 'provide a suitable filename given the nature of the notes. Prefer markdown extension unless otherwise instructed.',
        'evaluate_plots': False,
        'latest_plot_path': None,
        'latest_executed_code': None,
        'n_plot_evals': 0,
        'max_n_plot_evals': 1,
        'vlm_plot_analysis': None,
        'vlm_verdict': None,
        'plot_problems': [],
        'plot_fixes': [],
        'vlm_plot_structured_feedback': None,
        'work_dir': '/mnt/p/stage/cmbagent_benchmark/cmbagent_output/control',
        'needed_agents': ['engineer', 'researcher'],
        'cost_dataframe': Agent Cost($) Prompt Tokens Completion Tokens Total Tokens Model
        0 control 0.009010 4017.0 122.0 4139.0 gpt - 4.1 - 2025 - 04 - 14
        1 control starter 0.001308 650.0 1.0 651.0 gpt - 4.1 - 2025 - 04 - 14
        2 researcher 0.009994 2253.0 686.0 2939.0 gpt - 4.1 - 2025 - 04 - 14
        3 researcher response formatter 0.005012 996.0 890.0 1886.0 o3 - mini - 2025 - 01 - 31
        4 terminator 0.003936 1964.0 1.0 1965.0 gpt - 4.1 - 2025 - 04 - 14
        Total Total 0.029260 9880.0 1700.0 11580.0 NaN,
        'cost_report_path': '/mnt/p/stage/cmbagent_benchmark/cmbagent_output/control/cost/cost_report_step_2_20250805_123359.json',
        'transfer_to_idea_maker': False,
        'transfer_to_idea_hater': False,
        'transfer_to_classy_sz_agent': False,
        'transfer_to_planck_agent': False
    }),
    'initialization_time_control': 2.4902842044830322,
    'execution_time_control': 24.07383155822754
}
```

So here's how to extract relevant information from the provided context:
- code extraction: once the call i done, go to workdir/control/codebase/. Inside here will be only one .py file which contains the full code
- cost extraction: same as oneshot
- time extraction: same as oneshot
- token extraction: (technically isn't there but) same as oneshot (set to 0)
- example call:
result = cmbagent.planning_and_control_context_carryover(task,
                              max_rounds_control = 30,
                              n_plan_reviews = 1,
                              max_n_attempts = 2,
                              max_plan_steps=2,
                              engineer_model = "gemini-2.5-pro",
                              researcher_model = "gpt-4.1-2025-04-14",
                              plan_reviewer_model = "claude-sonnet-4-20250514", 
                              plan_instructions=r"""
Use engineer for whole analysis, and return final code with researcher at the very end. Plan must have between 3 and 5 steps.
""",
                            work_dir="/mnt/p/stage/cmbagent_benchmark/cmbagent_output/", # modify this accordingly
                            clear_work_dir = False,
                             )
- make sure to save work dir like oneshot does
- for now don't include anything about planning_and_control llm models, just implement the raw planning and control with
the default models you have in the example above.

## Planning_and_control agent support

### Usage
Add 'planning_and_control' as an agent name in your benchmark config. The system will run the planning_and_control agent using the default models and workflow as described below.

### Result Structure
After running, the planning_and_control agent will produce its output in the work directory:
- Code: Located in `workdir/control/codebase/` as a single `.py` file containing the full solution.
- Cost, time, and tokens: Extracted from the agent's result object, same as oneshot.

### Extraction Logic
- Code extraction: Read the `.py` file from `workdir/control/codebase/`.
- Cost extraction: Use the cost dataframe in the result object, same as oneshot.
- Time extraction: Use the timing info in the result object, same as oneshot.
- Token extraction: Not present, but handled as for oneshot (set to 0).

### Example config
```yaml
agents: [planning_and_control, oneshot-gpt-4.1-2025-04-14]
```

### Example call
```python
result = cmbagent.planning_and_control_context_carryover(
    task=task,
    max_rounds_control=30,
    plan_instructions=r"""
    Use engineer for whole analysis, and return final code with researcher at the very end. Plan must have between 3 and 5 steps.
    """,
    work_dir="/mnt/p/stage/cmbagent_benchmark/cmbagent_output/" # modify as needed
)
```

### Notes
- The benchmark runner will automatically create the work_dir and extract results as described above.

# ...existing code...


