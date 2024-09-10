import ast
import os

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

    @classmethod
    def from_file(cls, file_path):
        with open(file_path, 'r') as file:
            first_line = file.readline().strip()
            if first_line != "[Cyclic Voltammetry Config]":
                raise ValueError("Invalid file format: first line must be [Cyclic Voltammetry Config]")
            name = os.path.basename(file_path).split('.')[0]
            values = []
            for line in file:
                value = ast.literal_eval(line.split('=', 1)[1].strip())  # Evaluate the list
                values.append(value)                                                   # Append the value to the list
        return cls(name, values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7])

    @classmethod
    def from_cv_folder(cls):
        cv_dir = os.path.join(os.path.dirname(__file__), 'vcfgs', 'cv')
        cvs = {}
        for filename in os.listdir(cv_dir):
            if filename.endswith('.cv.vcfg'):
                file_path = os.path.join(cv_dir, filename)
                try:
                    cv_vcfg = cls.from_file(file_path)
                    cvs[cv_vcfg.name] = cv_vcfg
                except ValueError as ve:
                    print(f"Skipping file {filename}: {ve}")
        return cvs

    def __repr__(self):
        return (f"CV(name={self.name}, vs_init={self.vs_init}, v_step={self.v_step}, scan_rate={self.scan_rate}, "
                f"record_de={self.record_de}, average_de={self.average_de}, n_cycles={self.n_cycles}, "
                f"begin_i={self.begin_i}, end_i={self.end_i})")
