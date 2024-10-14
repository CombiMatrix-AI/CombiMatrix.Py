import ast
import os

import utils.experiment as experiment
from kbio import technique_fields


def from_file(file_path, file_type = None):
    with open(file_path, 'r') as file:
        if file_type is not None:
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
                    file = experiment.Block(*from_file(file_path, 'Block'))
                elif suffix == ".vcfg":
                    values = from_file(file_path)
                    file = experiment.Vcfg(values[0], values[1], getattr(technique_fields, values[1])(*values[2:]))
                elif suffix == ".gcode":
                    filename = os.path.basename(file_path)
                    file = experiment.Gcode(filename.split('.')[0], filename)
                else:
                    print(f"Unsupported file type: {suffix}")
                    return
                files[file.name] = file
            except ValueError as ve:
                print(f"Skipping file {filename}: {ve}")
    return files
