class Experiment:
    def __init__(self, block, technique, vcfg, gcode, tiled = 0):
        self.block = block
        self.technique = technique
        self.vcfg = vcfg
        self.gcode = gcode
        self.tiled = tiled

    def __str__(self):
        return (f'Block: {self.block.name[:9]:<10} Technique: {self.technique[:9]:<10} '
                f'Config: {self.vcfg.name[:9]:<10} Well: {self.gcode.split('.')[0][:9]:<10}')

