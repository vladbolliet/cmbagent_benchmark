# filename: codebase/main_function.py
def main_function(input_data: list[list[int | str]]):
    a = int(input_data[0][0])
    b = int(input_data[0][1])
    diff = abs(a - b)
    return [[diff]]
