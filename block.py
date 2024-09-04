import os


class Block:
    def __init__(self, block_id, num_rows, num_cols, start_row, start_column, definition):
        self.block_id = block_id
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.start_row = start_row
        self.start_column = start_column
        self.definition = definition

    @classmethod
    def from_file(cls, file_path):
        with open(file_path, 'r') as file:
            first_line = file.readline().strip()
            if first_line != "[Block]":
                raise ValueError("Invalid file format: first line must be [Block]")
            block_id = os.path.basename(file_path).split('.')[0]
            num_rows = num_cols = start_row = start_column = definition = None
            for line in file:
                if line.startswith('Number rows'):
                    num_rows = line.strip().split('=')[1].strip()
                elif line.startswith('Number columns'):
                    num_cols = line.strip().split('=')[1].strip()
                elif line.startswith('Start row'):
                    start_row = line.strip().split('=')[1].strip()
                elif line.startswith('Start column'):
                    start_column = line.strip().split('=')[1].strip()
                elif line.startswith('Definition'):
                    definition = line.strip().split('=')[1].strip()
            if not all([num_rows, num_cols, start_row, start_column, definition]):
                raise ValueError("File missing required block information")
        return cls(block_id, num_rows, num_cols, start_row, start_column, definition)

    @classmethod
    def from_blocks_folder(cls):
        blocks_dir = os.path.join(os.path.dirname(__file__), 'blocks')
        blocks = {}
        for filename in os.listdir(blocks_dir):
            if filename.endswith('.block'):
                file_path = os.path.join(blocks_dir, filename)
                try:
                    block = cls.from_file(file_path)
                    blocks[block.block_id] = block
                except ValueError as ve:
                    print(f"Skipping file {filename}: {ve}")
        return blocks

    def __repr__(self):
        return (f"Block(block_id={self.block_id}, num_rows={self.num_rows}, num_cols={self.num_cols}, "
                f"start_row={self.start_row}, start_column={self.start_column}, definition={self.definition})")
