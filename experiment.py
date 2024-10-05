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
    def __init__(self, solution, block=None, vcfg=None, gcode=None):
        self.solution = solution
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
        block_name = self.block.name if self.block else 'null'
        vcfg_technique = self.vcfg.technique if self.vcfg else 'null'
        vcfg_name = self.vcfg.name if self.vcfg else 'null'
        gcode_name = self.gcode.name if self.gcode else 'null'

        return (f'{self.solution[:24]:<25} Block: {block_name[:6]:<7} Mode: {vcfg_technique[:4]:<5} '
                f'Vcfg: {vcfg_name[:6]:<7} Well: {gcode_name[:6]:<7}')
