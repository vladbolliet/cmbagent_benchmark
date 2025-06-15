import os

def compare_problem_dirs(dir1, dir2):
    """
    Compare directory names (problem names) inside two parent directories.
    Prints any names that are missing from either directory.
    """
    # Get subdirectory names in both directories
    dir1_names = {name for name in os.listdir(dir1) if os.path.isdir(os.path.join(dir1, name))}
    dir2_names = {name for name in os.listdir(dir2) if os.path.isdir(os.path.join(dir2, name))}

    only_in_dir1 = dir1_names - dir2_names
    only_in_dir2 = dir2_names - dir1_names

    if not only_in_dir1 and not only_in_dir2:
        print("✅ All problem directories match.")
    else:
        print("❌ Mismatches found:")
        if only_in_dir1:
            print(f"- Present only in {dir1}:")
            for name in sorted(only_in_dir1):
                print(f"  {name}")
        if only_in_dir2:
            print(f"- Present only in {dir2}:")
            for name in sorted(only_in_dir2):
                print(f"  {name}")

import json

def compare_json_keys(file1, file2):
    """
    Compare the top-level keys of two JSON files.
    Prints any keys missing from either file.
    """
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    keys1 = set(data1.keys())
    keys2 = set(data2.keys())

    only_in_1 = keys1 - keys2
    only_in_2 = keys2 - keys1

    if not only_in_1 and not only_in_2:
        print("✅ All top-level keys match.")
    else:
        print("❌ Key mismatches found:")
        if only_in_1:
            print(f"- Present only in {file1}:")
            for key in sorted(only_in_1):
                print(f"  {key}")
        if only_in_2:
            print(f"- Present only in {file2}:")
            for key in sorted(only_in_2):
                print(f"  {key}")

import os
import json
import shutil

def clean_problem_directory(problem_dir, json_path):
    """
    Deletes all subdirectories in problem_dir that are not keys in the JSON dictionary at json_path.
    
    Parameters:
    - problem_dir: Path to the directory containing problem subdirectories.
    - json_path: Path to the JSON file containing valid problem keys.
    """
    # Load JSON keys
    with open(json_path, 'r') as f:
        valid_keys = set(json.load(f).keys())

    # List subdirectories in problem_dir
    for sub in os.listdir(problem_dir):
        sub_path = os.path.join(problem_dir, sub)
        if os.path.isdir(sub_path) and sub not in valid_keys:
            print(f"Deleting {sub_path} (not in JSON)...")
            shutil.rmtree(sub_path)

# Example usage:
# clean_problem_directory("/path/to/problems", "/path/to/keep_only_these.json")

import os
import json

def check_directory_matches_json(problem_dir, json_path):
    """
    Checks if all subdirectory names in problem_dir exactly match the keys in the JSON dictionary at json_path.
    Prints mismatches if found.
    """
    # Load JSON keys
    with open(json_path, 'r') as f:
        json_keys = set(json.load(f).keys())

    # Get all subdirectory names
    dir_names = set([
        name for name in os.listdir(problem_dir)
        if os.path.isdir(os.path.join(problem_dir, name))
    ])

    # Compute differences
    only_in_dirs = dir_names - json_keys
    only_in_json = json_keys - dir_names

    if not only_in_dirs and not only_in_json:
        print("✅ All subdirectories match JSON keys exactly.")
        return True
    else:
        if only_in_dirs:
            print("❌ Present in directory but missing in JSON:", sorted(only_in_dirs))
        if only_in_json:
            print("❌ Present in JSON but missing in directory:", sorted(only_in_json))
        return False

# Example usage:
# check_directory_matches_json("/path/to/problems", "/path/to/your_keys.json")


check_directory_matches_json("data/clean/usaco_tests", "data/clean/usaco_clean_307.json")
