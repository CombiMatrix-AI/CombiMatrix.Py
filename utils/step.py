from dataclasses import dataclass, field

@dataclass
class Block:
    name: str
    num_rows: int
    num_cols: int
    start_row: int
    start_col: int
    definition: list[list[int]] = field(default_factory=list)

@dataclass
class Vcfg:
    name: str
    technique: str
    configs: dict


class Step:
    def __init__(self, solution, stage, block=None, vcfg=None, gcode=None):
        self.solution = solution
        self.stage = stage
        self.block = block
        self.vcfg = vcfg
        self.gcode = gcode

    def tile_block(self):
        new_start_row = self.block.start_row
        new_start_col = self.block.start_col

        if self.block.start_col + self.block.num_cols * 2 <= 16:  # Check if we can place the block one block width to the right
            new_start_col = self.block.start_col + self.block.num_cols
        elif self.block.start_row - self.block.num_rows >= 0:  # If not, check if we can place it up
            new_start_row = self.block.start_row - self.block.num_rows
            new_start_col = self.block.start_col
            while new_start_col - self.block.num_cols >= 0:  # Push block to the left as much as possible
                new_start_col -= self.block.num_cols

        self.block = Block(self.block.name, self.block.num_rows,
                           self.block.num_cols, new_start_row, new_start_col, self.block.definition)

    def __str__(self):
        parts = [
            f'Soln: {self.solution[:15]:15}',
            f'Stage: {self.stage[:10]:10}',
            f'Block: {self.block.name[:10]:10}' if self.block else '',
            f'Mode: {self.vcfg.technique[:5]:5}' if self.vcfg else '',
            f'Vcfg: {self.vcfg.name[:10]:10}' if self.vcfg else '',
            f'Well: {self.gcode[:5]:5}' if self.gcode else ''
        ]
        return ' '.join(part for part in parts if part)
