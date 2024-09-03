import os

class Vcfg:
    def __init__(self, vcfg_id, func_type, va, vb, duration, period):
        self.vcfg_id = vcfg_id
        self.func_type = func_type
        self.va = va
        self.vb = vb
        self.duration = duration
        self.period = period

    @classmethod
    def from_file(cls, file_path):
        with open(file_path, 'r') as file:
            first_line = file.readline().strip()
            if first_line != "[Voltage Profile]":
                raise ValueError("Invalid file format: first line must be [Voltage Profile]")
            vcfg_id = os.path.basename(file_path).split('.')[0]
            func_type = va = vb = duration = period = None
            for line in file:
                if line.startswith('Type'):
                    func_type = line.strip().split('=')[1].strip()
                elif line.startswith('vA'):
                    va = line.strip().split('=')[1].strip()
                elif line.startswith('vB'):
                    vb = line.strip().split('=')[1].strip()
                elif line.startswith('Duration'):
                    duration = line.strip().split('=')[1].strip()
                elif line.startswith('Period'):
                    period = line.strip().split('=')[1].strip()
            if all([func_type, va, duration]) and func_type == 'Flat':
                vb = period = 0
            if not all([func_type, va, vb, duration, period]):
                raise ValueError("File missing required block information")
        return cls(vcfg_id, func_type, va, vb, duration, period)

    @classmethod
    def from_vcfgs_folder(cls):
        vcfgs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vcfgs')
        vcfgs = []
        for filename in os.listdir(vcfgs_dir):
            if filename.endswith('.vcfg'):
                file_path = os.path.join(vcfgs_dir, filename)
                try:
                    vcfg = cls.from_file(file_path)
                    vcfgs.append(vcfg)
                except ValueError as ve:
                    print(f"Skipping file {filename}: {ve}")
        return vcfgs

    def __repr__(self):
        return (f"Vcfg(vcfg_id={self.vcfg_id}, func_type={self.func_type}, va={self.va}, "
                f"vb={self.vb}, duration={self.duration}, period={self.period})")


