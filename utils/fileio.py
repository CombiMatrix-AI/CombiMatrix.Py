import ast

import utils.step as step
from kbio import technique_fields


def from_file(file_path, file_type = None):
    with open(file_path, 'r') as file:
        if file_type is not None:
            first_line = file.readline().strip()
            if first_line != f"[{file_type} Config]":
                raise ValueError(f"Invalid file format: first line must be [{file_type} Config]")
        values = []
        name = file_path.name.split('.')[0]
        values.append(name)
        for line in file:
            value = ast.literal_eval(line.split('=', 1)[1].strip())  # Evaluate the list
            values.append(value)  # Append the value to the list
    return values

def from_folder(path, suffix):
    files = {}
    for filename in path.iterdir():
        if filename.suffix == suffix:
            try:
                if suffix == ".block":
                    file = step.Block(*from_file(filename, 'Block'))
                elif suffix == ".vcfg":
                    values = from_file(filename)
                    file = step.Vcfg(values[0], values[1], getattr(technique_fields, values[1])(*values[2:]))
                elif suffix == ".gcode":
                    filename = filename.name
                    file = step.Gcode(filename.split('.')[0], filename)
                else:
                    print(f"Unsupported file type: {suffix}")
                    return
                files[file.name] = file
            except ValueError as ve:
                print(f"Skipping file {filename}: {ve}")
    return files
