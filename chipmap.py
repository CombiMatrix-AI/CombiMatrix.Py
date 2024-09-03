class ChipMap:
    def __init__(self):
        self.chipmap = [[0] * 16 for _ in range(64)]

    def from_block(self, block):
        num_rows = int(block.num_rows)
        num_cols = int(block.num_cols)
        start_row = int(block.start_row)
        start_col = int(block.start_column)
        definition = block.definition[1:-1] # remove quotation marks

        for i in range(num_rows):
            for j in range(num_cols):
                self.chipmap[start_row + i][start_col + j] = int(definition[i * num_cols + j])

        return self.chipmap

