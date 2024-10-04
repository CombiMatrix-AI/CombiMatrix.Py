from dataclasses import dataclass, field
from typing import Any


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
    configs: Any

@dataclass
class Gcode:
    name: str
    file: str

class Experiment:
    def __init__(self, solution, block, vcfg, gcode):
        self.solution: str = solution
        self.block: Block = block
        self.vcfg: Vcfg = vcfg
        self.gcode: Gcode = gcode

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
        return (f'{self.solution[:24]:<25} Block: {self.block.name[:6]:<7} Mode: {self.vcfg.technique[:4]:<5} '
                f'Vcfg: {self.vcfg.name[:6]:<7} Well: {self.gcode.name[:6]:<7}')

