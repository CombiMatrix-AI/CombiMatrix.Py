import os
import sys
import configparser
import random
import time
from ctypes import c_void_p
from PyQt6 import QtWidgets, QtCore
from qt_material import apply_stylesheet
from grbl_streamer import GrblStreamer

from block import Block
from cv import CV
#from adlink import Adlink
#from kbio import KBio
from view.gridwidget import GridWidget
from view.setupwindow import SetupWindow


def change_theme(theme):
    config = configparser.ConfigParser()
    config.read("config.ini")
    config.set('General', 'theme', theme)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    apply_stylesheet(QtWidgets.QApplication.instance(), theme=theme)

def execute_gcode(filename):
    gcode_dir = os.path.join(os.path.dirname(__file__), 'gcode', filename)
    with open(gcode_dir, 'r') as file:
        for line in file:
            grbl.send_immediately(line)
            time.sleep(10)

def grbl_callback(eventstring, *data):
    args = []
    for d in data:
        args.append(str(d))
    print("GRBL CALLBACK: event={} data={}".format(eventstring.ljust(30), ", ".join(args)))

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CombiMatrixAI")
        self.resize(800, 600)

        self.blocks = Block.from_blocks_folder()
        self.cvs = CV.from_cv_folder()

        self.setup_window = SetupWindow()
        self.setup_window.item_created.connect(self.item_created)

        self.setup_button = QtWidgets.QPushButton("Setup", self)
        self.setup_button.clicked.connect(self.setup_window.show)
        self.update_grid_button = QtWidgets.QPushButton("Update Block View", self)
        self.update_grid_button.clicked.connect(self.update_grid)
        self.chip_test_button = QtWidgets.QPushButton("Run Chip Test", self)
        self.chip_test_button.clicked.connect(lambda: self.chip_test(1))
        self.run_cv_button = QtWidgets.QPushButton("Run CV", self)
        self.run_cv_button.clicked.connect(lambda: ec_lab.cyclic_voltammetry(self.curr_cv))
        self.exit_button = QtWidgets.QPushButton("Exit", self)
        self.exit_button.clicked.connect(QtWidgets.QApplication.instance().quit)

        self.blocks_label = QtWidgets.QLabel("Load Block:", self)
        self.blocks_dropdown = QtWidgets.QComboBox(self)
        self.blocks_dropdown.addItems(list(self.blocks.keys()))
        self.blocks_dropdown.activated.connect(lambda: self.load_block(self.blocks_dropdown.currentText()))
        self.tile_block_button = QtWidgets.QPushButton("Tile Block", self)
        self.tile_block_button.clicked.connect(self.tile_block)
        self.cvs_label = QtWidgets.QLabel("Load CV Config:", self)
        self.cvs_dropdown = QtWidgets.QComboBox(self)
        self.cvs_dropdown.addItems(list(self.cvs.keys()))
        self.cvs_dropdown.activated.connect(lambda: self.load_cv(self.cvs_dropdown.currentText()))
        self.grid_widget = GridWidget()

        self.zero_button = QtWidgets.QPushButton("Zero Machine", self)
        self.zero_button.clicked.connect(lambda: execute_gcode("Zero"))
        self.a1_button = QtWidgets.QPushButton("Go to A1", self)
        self.a1_button.clicked.connect(lambda: execute_gcode("A1"))
        self.a2_button = QtWidgets.QPushButton("Go to A2", self)
        self.a2_button.clicked.connect(lambda: execute_gcode("A2"))
        self.a3_button = QtWidgets.QPushButton("Go to A3", self)
        self.a3_button.clicked.connect(lambda: execute_gcode("A3"))

        self.output_window = QtWidgets.QTextEdit(self)
        self.output_window.setReadOnly(True)
        self.output_window.setFixedSize(700, 500)

        self.theme_label = QtWidgets.QLabel("Theme:", self)
        self.theme_dropdown = QtWidgets.QComboBox(self)
        self.theme_dropdown.addItems(
            ['dark_amber.xml', 'dark_blue.xml', 'dark_cyan.xml', 'dark_lightgreen.xml', 'dark_pink.xml',
             'dark_purple.xml', 'dark_red.xml', 'dark_teal.xml', 'dark_yellow.xml', 'light_amber.xml', 'light_blue.xml',
             'light_cyan.xml', 'light_cyan_500.xml', 'light_lightgreen.xml', 'light_pink.xml', 'light_purple.xml',
             'light_red.xml', 'light_teal.xml', 'light_yellow.xml'])
        self.theme_dropdown.activated.connect(lambda: change_theme(self.theme_dropdown.currentText()))
        self.version_label = QtWidgets.QLabel("CombiMatrixAI, App Version: 090924 Alpha", self)
        self.version_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight)

        layout_master = QtWidgets.QVBoxLayout()

        layout_top = QtWidgets.QGridLayout()
        layout_top.addWidget(self.setup_button, 0, 0)
        layout_top.addWidget(self.update_grid_button, 0, 1)
        layout_top.addWidget(self.chip_test_button, 0, 2)
        layout_top.addWidget(self.run_cv_button, 0, 3)
        spacer_top = QtWidgets.QSpacerItem(100, 0, QtWidgets.QSizePolicy.Policy.Fixed,
                                       QtWidgets.QSizePolicy.Policy.Fixed)
        layout_top.addItem(spacer_top, 0, 4)
        layout_top.addWidget(self.exit_button, 0, 5)
        layout_master.addLayout(layout_top)

        layout_middle = QtWidgets.QHBoxLayout()
        layout_middle_grid = QtWidgets.QGridLayout()
        layout_middle_grid.addWidget(self.blocks_label, 0, 0)
        layout_middle_grid.addWidget(self.blocks_dropdown, 0, 1)
        layout_middle_grid.addWidget(self.tile_block_button, 0, 2)
        layout_middle_grid.addWidget(self.cvs_label, 1, 0)
        layout_middle_grid.addWidget(self.cvs_dropdown, 1, 1)
        layout_middle_grid.addWidget(self.zero_button, 2, 0)
        layout_middle_grid.addWidget(self.a1_button, 2, 1)
        layout_middle_grid.addWidget(self.a2_button, 2, 2)
        layout_middle_grid.addWidget(self.a3_button, 2, 3)
        spacer = QtWidgets.QSpacerItem(125, 150, QtWidgets.QSizePolicy.Policy.Fixed,
                                       QtWidgets.QSizePolicy.Policy.Minimum)
        layout_middle_grid.addItem(spacer, 3, 0)
        layout_middle_grid.addItem(spacer, 3, 1)
        layout_middle_grid.addItem(spacer, 3, 2)
        layout_middle_grid.addItem(spacer, 3, 3)
        layout_middle.addLayout(layout_middle_grid)
        layout_middle.addWidget(self.output_window)
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



    def item_created(self, text): # TODO: MAYBE HAVE LIST GO TO NEW BLOCK UPON CREATING NEW BLOCK?
        if text.split(',')[0].strip() == "Block Created":
            self.blocks = Block.from_blocks_folder()
            self.blocks_dropdown.clear()
            self.blocks_dropdown.addItems(list(self.blocks.keys()))
            new_index = self.blocks_dropdown.findText(text.split(',')[1].strip())
            self.blocks_dropdown.setCurrentIndex(new_index)
            self.load_block(self.blocks_dropdown.currentText())  # Ensure something is loaded when program starts
        elif text.split(',')[0].strip() == "CV Config Created":
            self.cvs = CV.from_cv_folder()
            self.cvs_dropdown.clear()
            self.cvs_dropdown.addItems(list(self.cvs.keys()))
            new_index = self.cvs_dropdown.findText(text.split(',')[1].strip())
            self.cvs_dropdown.setCurrentIndex(new_index)
            self.load_cv(self.cvs_dropdown.currentText())

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

        adlink_card.set_chip_map(channel, chipmap_in)
        chipmap_out = adlink_card.get_chip_map(channel)

        for row in range(64):
            for column in range(16):
                match chipmap_in[row][column], chipmap_out[row][column]:
                    case (0, 0):
                        self.grid_widget.set_square_color(row, column, 'grey')
                    case (1, 1):
                        self.grid_widget.set_square_color(row, column, 'blue')
                    case (2, 2):
                        self.grid_widget.set_square_color(row, column, 'yellow')
                    case (3, 3):
                        self.grid_widget.set_square_color(row, column, 'green')
                    case _:
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
            for row, col, value1, value2 in differences:
                print(f"Row {row}, Col {col}: chipmap_in has {value1}, chipmap_out has {value2}")

    def load_block(self, block):
        # Logic for loading the block
        print(f"Block loaded: {block}")
        self.grid_widget.clear()
        self.curr_block = self.blocks[block]

        definition = self.curr_block.definition[1:-1]  # remove quotation marks

        currmap = [[0] * 16 for _ in range(64)]
        for i in range(self.curr_block.num_rows):
            for j in range(self.curr_block.num_cols):
                currmap[self.curr_block.start_row + i][self.curr_block.start_column + j] = int(definition[i * self.curr_block.num_cols + j])
                if currmap[self.curr_block.start_row + i][self.curr_block.start_column + j] == 2:
                    self.grid_widget.set_square_color(self.curr_block.start_row + i, self.curr_block.start_column + j, 'yellow')

        #adlink_card.set_chip_map(1, currmap)

    def tile_block(self):
        if self.curr_block is None:
            return
        print(f"Block tiled: {self.curr_block}")
        self.grid_widget.clear()

        definition = self.curr_block.definition[1:-1]  # remove quotation marks
        new_start_row = self.curr_block.start_row
        new_start_col = self.curr_block.start_column

        if self.curr_block.start_column + self.curr_block.num_cols * 2 <= 16:  # Check if we can place the block one block width to the right
            new_start_col = self.curr_block.start_column + self.curr_block.num_cols
        elif self.curr_block.start_row - self.curr_block.num_rows >= 0:  # If not, check if we can place it up
            new_start_row = self.curr_block.start_row - self.curr_block.num_rows
            new_start_col = self.curr_block.start_column
            while new_start_col - self.curr_block.num_cols >= 0:  # Push block to the left as much as possible
                new_start_col -= self.curr_block.num_cols

        currmap = [[0] * 16 for _ in range(64)]
        for i in range(self.curr_block.num_rows):         # Place the block
            for j in range(self.curr_block.num_cols):
                currmap[new_start_row + i][new_start_col + j] = int(definition[i * self.curr_block.num_cols + j])
                if currmap[new_start_row + i][new_start_col + j] == 2:
                    self.grid_widget.set_square_color(new_start_row + i, new_start_col + j, 'yellow')


        self.curr_block = Block(self.curr_block.block_id, self.curr_block.num_rows,
                                      self.curr_block.num_cols, new_start_row, new_start_col, self.curr_block.definition)
        #adlink_card.set_chip_map(1, currmap)

    def load_cv(self, cv):
        # Logic for loading the cv config
        print(f"CV Config loaded: {cv}")
        self.curr_cv = self.cvs[cv]

    def write(self, text):
        self.output_window.append(text.rstrip())


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")

    app = QtWidgets.QApplication(sys.argv)
    theme = config.get('General', 'theme')
    apply_stylesheet(app, theme=theme)

    main_window = MainWindow()
    sys.stdout = main_window  # Now, redirect standard output to our text widget
    main_window.show()
    main_window.load_block(main_window.blocks_dropdown.currentText())  # Ensure something is loaded when program starts
    main_window.load_cv(main_window.cvs_dropdown.currentText())

    #adlink_card = Adlink()

    kbio_port = config.get('Ports', 'vmp3_port')
    #ec_lab = KBio(kbio_port)

    grbl = GrblStreamer(grbl_callback)
    grbl.setup_logging()
    grbl_port = config.get('Ports', 'grbl_port')
    #grbl.cnect(grbl_port, 115200)

    app.exec()

    # Cleanup funcs
    adlink_card.release_adlink()
    ec_lab.release_kbio()
    grbl.disconnect()