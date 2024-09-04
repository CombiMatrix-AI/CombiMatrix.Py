import configparser
import random

from PyQt6 import QtWidgets, QtCore
from qt_material import apply_stylesheet

from view.gridwidget import GridWidget
from view.setupwindow import SetupWindow


from init import *


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CombiMatrixAI")
        self.resize(800, 600)  # Bigger is better!!
        self.setup_window = SetupWindow()

        self.setup_button = QtWidgets.QPushButton("Setup", self)
        self.setup_button.setGeometry(50, 50, 100, 30)
        self.setup_button.clicked.connect(self.setup_window.show)
        self.grid_widget = GridWidget()

        self.version_label = QtWidgets.QLabel("CombiMatrixAI, App Version: 0.001", self)
        self.version_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight)

        self.theme_label = QtWidgets.QLabel("Theme:", self)
        self.theme_dropdown = QtWidgets.QComboBox(self)
        self.theme_dropdown.addItems(['dark_amber.xml', 'dark_blue.xml', 'dark_cyan.xml', 'dark_lightgreen.xml',
                                      'dark_pink.xml', 'dark_purple.xml', 'dark_red.xml', 'dark_teal.xml',
                                      'dark_yellow.xml', 'light_amber.xml', 'light_blue.xml', 'light_cyan.xml',
                                      'light_cyan_500.xml', 'light_lightgreen.xml', 'light_pink.xml',
                                      'light_purple.xml', 'light_red.xml', 'light_teal.xml', 'light_yellow.xml'])
        self.theme_dropdown.activated.connect(lambda: self.change_theme(self.theme_dropdown.currentText()))

        self.blocks_label = QtWidgets.QLabel("Load Block:", self)
        self.blocks_dropdown = QtWidgets.QComboBox(self)
        self.blocks_dropdown.addItems(list(blocks.keys()))
        self.blocks_dropdown.activated.connect(lambda: self.load_block(self.blocks_dropdown.currentText()))

        self.chip_test_button = QtWidgets.QPushButton("Run Chip Test", self)
        self.chip_test_button.clicked.connect(lambda: self.chip_test(1))

        layout = QtWidgets.QHBoxLayout()

        # TODO: pls fix my horrible layout
        layout.addWidget(self.setup_button, 0, QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.theme_label, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.theme_dropdown, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.blocks_label, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.blocks_dropdown, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.chip_test_button, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.grid_widget, 0,
                         QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight)  # Place the grid widget next to the other widgets
        layout.addWidget(self.version_label, 0,
                         QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight)

        container = QtWidgets.QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def change_theme(self, theme):
        config = configparser.ConfigParser()
        config.read("config.ini")
        config.set('General', 'theme', theme)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        apply_stylesheet(QtWidgets.QApplication.instance(), theme=theme)

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
                chipmap_in = [[1 if j % 2 == 0 else 2 for j in range(16)] for _ in range(64)]
            elif i == 5:
                chipmap_in = [[2 if j % 2 == 0 else 3 for j in range(16)] for _ in range(64)]
            elif i == 6:
                chipmap_in = [[random.randint(0, 3)] * 16 for _ in range(64)]

            chipmap_out = [[0] * 16 for _ in range(64)]

            adlink.set_chip_map(channel, chipmap_in)
            adlink.get_chip_map(channel, chipmap_out)

            if chipmap_in == chipmap_out:
                print(f"Test {i} Passed")
            else:
                print(f"Test {i} Failed")
                differences = [(l, chipmap_in[l], chipmap_out[l]) for l in range(len(chipmap_in)) if
                               chipmap_in[l] != chipmap_out[l]]
                # Print differences
                for index, value1, value2 in differences:
                    print(f"Index {index}: list1 has {value1}, list2 has {value2}")

    def load_block(self, block):
        # Logic for loading the block
        print(f"Block loaded: {block}")
        chipmap.clear()
        self.grid_widget.clear()

        chipmap.from_block(blocks[block])

        output = chipmap.output()

        for row in range(64):
            for column in range(16):
                if output[row][column] == 2:
                    self.grid_widget.set_square_color(row, column, 'yellow')

        adlink.set_chip_map(1, output)
