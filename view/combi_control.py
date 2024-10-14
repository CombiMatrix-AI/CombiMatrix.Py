import os
import platform
import random

from PyQt6.QtWidgets import QMainWindow, QPushButton, QComboBox, QWidget, QGridLayout, QApplication

from utils import fileio

if platform.system() != 'Darwin':
    from utils.adlink import Adlink
from utils.ui_utils import ROOT_DIR
from view.create_block import CreateBlockWindow
from view.grid_widget import GridWidget
from utils.experiment import Block


class CombiControlWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Combi Chip Control")

        if platform.system() != 'Darwin':
            self.adlink_card = Adlink()
        print("DEBUG MESSAGE: Adlink Card Initialized")

        self.blocks_dir = os.path.join(ROOT_DIR, 'blocks')
        self.blocks = fileio.from_folder(self.blocks_dir, '.block')

        self.create_block_window = CreateBlockWindow()
        self.create_block_window.item_created.connect(self.item_created)

        self.blocks_dropdown = QComboBox(self)
        self.blocks_dropdown.addItems(list(self.blocks.keys()))

        self.create_block_button = QPushButton("Create Block", self)
        self.create_block_button.clicked.connect(self.create_block_window.show)
        
        chip_test_button = QPushButton("Run Chip Test", self)
        chip_test_button.clicked.connect(self.chip_test)
        
        tile_block_button = QPushButton("Tile Block", self)
        tile_block_button.clicked.connect(self.tile_block)
        
        load_block_button = QPushButton("Load Block", self)
        load_block_button.clicked.connect(lambda: self.load_block(self.current_block))
        self.blocks_dropdown = QComboBox(self)
        self.blocks_dropdown.setFixedWidth(200)  # Set the width of the block dropdown
        self.blocks_dropdown.addItems(list(self.blocks.keys()))
        self.blocks_dropdown.currentIndexChanged.connect(self.on_block_changed)

        exit_button = QPushButton("Exit", self)
        exit_button.clicked.connect(QApplication.instance().quit)
        
        self.grid_widget = GridWidget(5)
        
        self.current_block = self.blocks[self.blocks_dropdown.currentText()]

        ############################### WINDOW LAYOUT #################################

        layout_master = QGridLayout()
        layout_master.addWidget(load_block_button, 0, 0)
        layout_master.addWidget(self.blocks_dropdown, 0, 1)
        layout_master.addWidget(tile_block_button, 1, 0)
        layout_master.addWidget(self.create_block_button, 2, 0)
        layout_master.addWidget(exit_button, 3, 0)
        layout_master.addWidget(self.grid_widget, 0, 2, 4, 1)  # Place the grid widget next to the other widgets

        container = QWidget()
        container.setLayout(layout_master)
        self.setCentralWidget(container)

    def on_block_changed(self):
        if self.blocks_dropdown.currentText() in self.blocks:
            self.current_block = self.blocks[self.blocks_dropdown.currentText()]

    def item_created(self, text):
        self.blocks = fileio.from_folder(self.blocks_dir, '.block')
        self.blocks_dropdown.clear()
        self.blocks_dropdown.addItems(list(self.blocks.keys()))
        new_index = self.blocks_dropdown.findText(text.split(',')[1].strip())
        self.blocks_dropdown.setCurrentIndex(new_index)

    def tile_block(self):
        new_start_row = self.current_block.start_row
        new_start_col = self.current_block.start_col

        if self.current_block.start_col + self.current_block.num_cols * 2 <= 16:  # Check if we can place the block one block width to the right
            new_start_col = self.current_block.start_col + self.current_block.num_cols
        elif self.current_block.start_row - self.current_block.num_rows >= 0:  # If not, check if we can place it up
            new_start_row = self.current_block.start_row - self.current_block.num_rows
            new_start_col = self.current_block.start_col
            while new_start_col - self.current_block.num_cols >= 0:  # Push block to the left as much as possible
                new_start_col -= self.current_block.num_cols

        self.current_block = Block(self.current_block.name, self.current_block.num_rows,
                           self.current_block.num_cols, new_start_row, new_start_col, self.current_block.definition)

        self.load_block(self.current_block)

    def load_block(self, block):
        # Logic for loading the block
        self.grid_widget.clear()
        current_map = [[0] * 16 for _ in range(64)]
        for i in range(block.num_rows):
            for j in range(block.num_cols):
                current_map[block.start_row + i][block.start_col + j] = block.definition[i][j]
                self.grid_widget.set_square_color(block.start_row + i, block.start_col + j,
                                                  current_map[block.start_row + i][block.start_col + j])
        if platform.system() != 'Darwin':
            self.adlink_card.set_chip_map(1, current_map)
        print(f"{block} loaded")
            
    def chip_test(self):
        channel = 1

        for i in range(7):
            match i:
                case 0:
                    chipmap_in = [[0] * 16 for _ in range(64)]
                case 1:
                    chipmap_in = [[1] * 16 for _ in range(64)]
                case 2:
                    chipmap_in = [[2] * 16 for _ in range(64)]
                case 3:
                    chipmap_in = [[3] * 16 for _ in range(64)]
                case 4:
                    chipmap_in = [[1 if (r + c) % 2 == 0 else 2 for c in range(16)] for r in range(64)]
                case 5:
                    chipmap_in = [[2 if (r + c) % 2 == 0 else 3 for c in range(16)] for r in range(64)]
                case 6:
                    chipmap_in = [[random.randint(0, 3) for _ in range(16)] for _ in range(64)]
                case _:
                    break

        self.adlink_card.set_chip_map(channel, chipmap_in)
        chipmap_out = self.adlink_card.get_chip_map(channel)

        for row in range(64):
            for column in range(16):
                self.grid_widget.set_square_color(row, column,
                                                  chipmap_in[row][column], chipmap_out[row][column])

        if chipmap_in == chipmap_out:
            print(f"Test {i} Passed")
        else:
            print(f"Test {i} Failed")
            differences = [
                (r, c, chipmap_in[r][c], chipmap_out[r][c])
                for r in range(len(chipmap_in))
                for c in range(len(chipmap_in[r]))
                if chipmap_in[r][c] != chipmap_out[r][c]
            ]
            for row, col, value1, value2 in differences:
                print(f"Row {row}, Col {col}: chipmap_in has {value1}, chipmap_out has {value2}")



