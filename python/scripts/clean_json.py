"""

This script does the following:

1. Load a json file (usaco_subset307_dict.json or usaco_v2_dict.json)

2. Keep only: problem_id, problem_level, description, num_tests

3. Save cleaned version as usaco_clean_307.json or usaco_clean_all.json to data/clean/

Observation: in order to obtain the clean version of a .json file you have to manually enter the input_path and output_path of your .json file 

"""

import json  # to load and save JSON files
import os    # to handle file paths and directories

# Define input and output file paths
input_path = "../../data/datasets/usaco_subset307_dict.json"  # original JSON file
output_dir = "../../data/clean"  # directory to save cleaned JSON
output_path = os.path.join(output_dir, "usaco_clean_307.json")  # cleaned file path

# Ensure the output directory exists; if not, create it
os.makedirs(output_dir, exist_ok=True)

# Open (in read mode) and load the original JSON file into a Python dictionary
with open(input_path, "r") as f:
    data = json.load(f)  # 'data' is a dict: keys=problem_id, value=dict with all the fields

# Create a new dict with only selected keys for each problem
cleaned_data = {}
for pid, problem in data.items():  # iterate over each problem by id and data
    cleaned_data[pid] = {
        "problem_id": problem.get("problem_id"),          # problem identifier
        "problem_level": problem.get("problem_level"),    # difficulty level
        "description": problem.get("description"),        # problem statement text
        "num_tests": problem.get("num_tests")             # number of test input-output pairs
    }

# Save the cleaned dictionary to a new JSON file
with open(output_path, "w") as f:
    json.dump(cleaned_data, f, indent=2)  # pretty-print with indentation
