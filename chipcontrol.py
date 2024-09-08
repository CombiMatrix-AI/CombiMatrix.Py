def from_block(block, chipmap):
    num_rows = int(block.num_rows)
    num_cols = int(block.num_cols)
    start_row = int(block.start_row)
    start_col = int(block.start_column)
    definition = block.definition[1:-1] # remove quotation marks

    for i in range(num_rows):
        for j in range(num_cols):
            chipmap[start_row + i][start_col + j] = int(definition[i * num_cols + j])

    return chipmap

def tile_block(block, chipmap):
    num_rows = int(block.num_rows)
    num_cols = int(block.num_cols)
    start_row = int(block.start_row)
    start_col = int(block.start_column)
    definition = block.definition[1:-1]  # remove quotation marks

    new_start_row = start_row
    new_start_col = start_col

    # Check if we can place the block one block width to the right
    if start_col + num_cols * 2 <= 16:
        new_start_col = start_col + num_cols
    # If not, check if we can place it up and to the left
    elif start_row - num_rows >= 0:
        new_start_row = start_row - num_rows
        if start_col - num_cols >= 0:
            new_start_col = start_col - num_cols
        else:
            new_start_col = start_col
        while new_start_col - num_cols >= 0:
            new_start_col -= num_cols

    # Place the block
    for i in range(num_rows):
        for j in range(num_cols):
            chipmap[new_start_row + i][new_start_col + j] = int(definition[i * num_cols + j])

    return chipmap, new_start_row, new_start_col

