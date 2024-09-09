import sys
import configparser
import random
from PyQt6 import QtWidgets, QtCore
from qt_material import apply_stylesheet
from grbl_streamer import GrblStreamer

from block import Block
from adlink import Adlink
from kbio import KBio
from view.gridwidget import GridWidget
from view.outputlog import OutputWindow
from view.setupwindow import SetupWindow

def grbl_callback(eventstring, *data):
    args = []
    for d in data:
        args.append(str(d))
    print("GRBL CALLBACK: event={} data={}".format(eventstring.ljust(30), ", ".join(args)))

def change_theme(theme):
    config = configparser.ConfigParser()
    config.read("config.ini")
    config.set('General', 'theme', theme)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    apply_stylesheet(QtWidgets.QApplication.instance(), theme=theme)

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

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, output_window):
        super().__init__()
        self.setWindowTitle("CombiMatrixAI")
        self.resize(800, 600)

        self.blocks = Block.from_blocks_folder()
        self.curr_block = None

        self.setup_window = SetupWindow()
        self.setup_window.block_created.connect(self.update_blocks)

        self.setup_button = QtWidgets.QPushButton("Setup", self)
        self.setup_button.clicked.connect(self.setup_window.show)
        self.update_grid_button = QtWidgets.QPushButton("Update Block View", self)
        self.update_grid_button.clicked.connect(self.update_grid)
        self.chip_test_button = QtWidgets.QPushButton("Run Chip Test", self)
        self.chip_test_button.clicked.connect(lambda: self.chip_test(1))
        self.output_window_button = QtWidgets.QPushButton("Open Output Window", self)
        self.output_window_button.clicked.connect(lambda: output_window.show())
        self.exit_button = QtWidgets.QPushButton("Exit", self)
        self.exit_button.clicked.connect(QtWidgets.QApplication.instance().quit)

        self.blocks_label = QtWidgets.QLabel("Load Block:", self)
        self.blocks_dropdown = QtWidgets.QComboBox(self)
        self.blocks_dropdown.addItems(list(self.blocks.keys()))
        self.blocks_dropdown.activated.connect(lambda: self.load_block(self.blocks_dropdown.currentText()))
        self.tile_block_button = QtWidgets.QPushButton("Tile Block", self)
        self.tile_block_button.clicked.connect(self.tile_block)
        self.grid_widget = GridWidget()

        self.theme_label = QtWidgets.QLabel("Theme:", self)
        self.theme_dropdown = QtWidgets.QComboBox(self)
        self.theme_dropdown.addItems(
            ['dark_amber.xml', 'dark_blue.xml', 'dark_cyan.xml', 'dark_lightgreen.xml', 'dark_pink.xml',
             'dark_purple.xml', 'dark_red.xml', 'dark_teal.xml', 'dark_yellow.xml', 'light_amber.xml', 'light_blue.xml',
             'light_cyan.xml', 'light_cyan_500.xml', 'light_lightgreen.xml', 'light_pink.xml', 'light_purple.xml',
             'light_red.xml', 'light_teal.xml', 'light_yellow.xml'])
        self.theme_dropdown.activated.connect(lambda: change_theme(self.theme_dropdown.currentText()))
        self.version_label = QtWidgets.QLabel("CombiMatrixAI, App Version: 0.1", self)
        self.version_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight)

        layout_master = QtWidgets.QVBoxLayout()

        layout_top = QtWidgets.QGridLayout()
        layout_top.addWidget(self.setup_button, 0, 0)
        layout_top.addWidget(self.update_grid_button, 0, 1)
        layout_top.addWidget(self.chip_test_button, 0, 2)
        layout_top.addWidget(self.output_window_button, 0, 3)
        layout_top.addWidget(self.exit_button, 0, 6)
        layout_master.addLayout(layout_top)

        layout_middle = QtWidgets.QHBoxLayout()
        layout_middle.addWidget(self.blocks_label, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout_middle.addWidget(self.blocks_dropdown, 5, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout_middle.addWidget(self.tile_block_button, 7, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout_middle.addWidget(self.grid_widget, 0,
                         QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight)  # Place the grid widget next to the other widgets
        layout_master.addLayout(layout_middle)

        layout_bottom = QtWidgets.QHBoxLayout()
        layout_bottom.addWidget(self.theme_label, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout_bottom.addWidget(self.theme_dropdown, 10, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout_bottom.addWidget(self.version_label, 0,
                         QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight)
        layout_master.addLayout(layout_bottom)

        container = QtWidgets.QWidget()
        container.setLayout(layout_master)
        self.setCentralWidget(container)

    def update_blocks(self):
        self.blocks = Block.from_blocks_folder()
        self.blocks_dropdown.clear()
        self.blocks_dropdown.addItems(list(self.blocks.keys()))

    def update_grid(self):
        self.grid_widget.clear()

        currmap = adlink_card.get_chip_map(1) # TODO: ACCOUNT FOR MULTI CHANNEL

        for row in range(64):
            for column in range(16):
                if currmap[row][column] == 0:
                    self.grid_widget.set_square_color(row, column, 'grey')
                if currmap[row][column] == 1:
                    self.grid_widget.set_square_color(row, column, 'blue')
                if currmap[row][column] == 2:
                    self.grid_widget.set_square_color(row, column, 'yellow')
                if currmap[row][column] == 3:
                    self.grid_widget.set_square_color(row, column, 'green')

    def chip_test(self, channel):
        for i in range(7):
            if i == 0:
                chipmap_in = [[0] * 16 for _ in range(64)]
            elif i == 1:
                chipmap_in = [[1] * 16 for _ in range(64)]
            elif i == 2:
                chipmap_in = [[2] * 16 for _ in range(64)]
            elif i == 3:
                chipmap_in = [[3] * 16 for _ in range(64)]
            elif i == 4:
                chipmap_in = [[1 if (r + c) % 2 == 0 else 2 for c in range(16)] for r in range(64)]
            elif i == 5:
                chipmap_in = [[2 if (r + c) % 2 == 0 else 3 for c in range(16)] for r in range(64)]
            elif i == 6:
                chipmap_in = [[random.randint(0, 3) for _ in range(16)] for _ in range(64)]
            else:  # Handle out of bounds cases
                break

            adlink_card.set_chip_map(channel, chipmap_in)
            chipmap_out = adlink_card.get_chip_map(channel)

            for row in range(64):
                for column in range(16):
                    if chipmap_in[row][column] == chipmap_out[row][column] == 0:
                        self.grid_widget.set_square_color(row, column, 'grey')
                    if chipmap_in[row][column] == chipmap_out[row][column] == 1:
                        self.grid_widget.set_square_color(row, column, 'blue')
                    if chipmap_in[row][column] == chipmap_out[row][column] == 2:
                        self.grid_widget.set_square_color(row, column, 'yellow')
                    if chipmap_in[row][column] == chipmap_out[row][column] == 3:
                        self.grid_widget.set_square_color(row, column, 'green')
                    else:
                        self.grid_widget.set_square_color(row, column, 'red')

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
                # Print differences
                for row, col, value1, value2 in differences:
                    print(f"Row {row}, Col {col}: chipmap_in has {value1}, chipmap_out has {value2}")

    def load_block(self, block):
        # Logic for loading the block
        print(f"Block loaded: {block}")
        self.grid_widget.clear()
        self.curr_block = self.blocks[block]

        currmap = from_block(self.blocks[block], [[0] * 16 for _ in range(64)])

        for row in range(64):
            for column in range(16):
                if currmap[row][column] == 2:
                    self.grid_widget.set_square_color(row, column, 'yellow')

        adlink_card.set_chip_map(1, currmap)

    def tile_block(self):
        if self.curr_block is None:
            return
        old_block = self.curr_block
        print(f"Block tiled: {old_block}")
        self.grid_widget.clear()

        currmap, new_start_row, new_start_column = tile_block(old_block, [[0] * 16 for _ in range(64)])

        self.curr_block = Block(old_block.block_id, old_block.num_rows,
                                      old_block.num_cols, new_start_row, new_start_column, old_block.definition)

        for row in range(64):
            for column in range(16):
                if currmap[row][column] == 2:
                    self.grid_widget.set_square_color(row, column, 'yellow')

        adlink_card.set_chip_map(1, currmap)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")

    app = QtWidgets.QApplication(sys.argv)
    theme = config.get('General', 'theme')
    apply_stylesheet(app, theme=theme)

    output_window = OutputWindow()
    output_window.show()
    sys.stdout = output_window  # Now, redirect standard output to our text widget
    main_window = MainWindow(output_window)
    main_window.show()

    adlink_card = Adlink()
    adlink_card.set_chip_map(1, [[0] * 16 for _ in range(64)]) # Zero chip # TODO: UPDATE FOR MULTIPLE CHANNELS

    kbio_port = config.get('General', 'vmp3_port')
    ec_lab = KBio(kbio_port)

    grbl = GrblStreamer(grbl_callback)
    grbl.setup_logging()
    grbl_port = config.get('General', 'grbl_port')
    grbl.cnect(grbl_port, 115200)

    app.exec()

    # Cleanup funcs
    adlink_card.release_adlink()
    ec_lab.release_kbio()
    grbl.disconnect()