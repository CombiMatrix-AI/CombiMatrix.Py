import ast
import os

def from_file(file_path, file_type):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
        if first_line != f"[{file_type} Config]":
            raise ValueError(f"Invalid file format: first line must be [{file_type} Config]")
        values = []
        name = os.path.basename(file_path).split('.')[0]
        values.append(name)
        for line in file:
            value = ast.literal_eval(line.split('=', 1)[1].strip())  # Evaluate the list
            values.append(value)  # Append the value to the list
    return values

def from_folder(path, suffix):
    files = {}
    for filename in os.listdir(path):
        if filename.endswith(suffix):
            file_path = os.path.join(path, filename)
            try:
                if suffix == ".block":
                    file = Block(*from_file(file_path, 'Block'))
                    files[file.name] = file
                elif suffix == ".cv.vcfg":
                    file = CV(*from_file(file_path, 'Cyclic Voltammetry'))
                    files[file.name] = file
                else: # suffix == ".gcode"
                    file = os.path.basename(file_path)
                    files[file.split('.')[0]] = file
            except ValueError as ve:
                print(f"Skipping file {filename}: {ve}")
    return files

class CV:
    def __init__(self, name, vs_init, v_step, scan_rate, record_de, average_de, n_cycles, begin_i, end_i):
        self.name = name
        self.vs_init = vs_init
        self.v_step = v_step
        self.scan_rate = scan_rate
        self.record_de = record_de
        self.average_de = average_de
        self.n_cycles = n_cycles
        self.begin_i = begin_i
        self.end_i = end_i

class Block:
    def __init__(self, name, num_rows, num_cols, start_row, start_column, definition):
        self.name = name
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.start_row = start_row
        self.start_column = start_column
        self.definition = definition
