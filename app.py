import sys
import configparser
from PyQt6 import QtWidgets, QtCore
from qt_material import apply_stylesheet

from view.outputlog import OutputWindow
from view.gridwidget import GridWidget
from view.setupwindow import SetupWindow
import block
import chipcontrol
import chipmap

adlink = chipcontrol.Adlink()
chipmap = chipmap.ChipMap()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CombiMatrixAI")
        self.resize(800, 600)  # Bigger is better!!
        self.setup_window = SetupWindow()
        self.blocks = block.Block.from_blocks_folder()

        self.setup_window.block_created.connect(self.update_blocks)

        self.setup_button = QtWidgets.QPushButton("Setup", self)
        self.setup_button.setGeometry(50, 50, 100, 30)
        self.setup_button.clicked.connect(self.setup_window.show)
        self.grid_widget = GridWidget()

        self.version_label = QtWidgets.QLabel("CombiMatrixAI, App Version: 0.1", self)
        self.version_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight)

        self.theme_label = QtWidgets.QLabel("Theme:", self)
        self.theme_dropdown = QtWidgets.QComboBox(self)
        self.theme_dropdown.addItems(
            ['dark_amber.xml', 'dark_blue.xml', 'dark_cyan.xml', 'dark_lightgreen.xml', 'dark_pink.xml',
             'dark_purple.xml', 'dark_red.xml', 'dark_teal.xml', 'dark_yellow.xml', 'light_amber.xml', 'light_blue.xml',
             'light_cyan.xml', 'light_cyan_500.xml', 'light_lightgreen.xml', 'light_pink.xml', 'light_purple.xml',
             'light_red.xml', 'light_teal.xml', 'light_yellow.xml'])
        self.theme_dropdown.activated.connect(lambda: self.change_theme(self.theme_dropdown.currentText()))

        self.blocks_label = QtWidgets.QLabel("Load Block:", self)
        self.blocks_dropdown = QtWidgets.QComboBox(self)
        self.blocks_dropdown.addItems(list(self.blocks.keys()))
        self.blocks_dropdown.activated.connect(lambda: self.load_block(self.blocks_dropdown.currentText()))

        self.chip_test_button = QtWidgets.QPushButton("Run Chip Test", self)
        self.chip_test_button.clicked.connect(lambda: adlink.chip_test(1))

        self.exit_button = QtWidgets.QPushButton("Exit", self)
        self.exit_button.clicked.connect(QtWidgets.QApplication.instance().quit)

        layout = QtWidgets.QHBoxLayout()

        # TODO: pls fix my horrible layout
        layout.addWidget(self.setup_button, 0, QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.chip_test_button, 0, QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.exit_button, 0, QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.theme_label, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.theme_dropdown, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.blocks_label, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.blocks_dropdown, 0, QtCore.Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(self.grid_widget, 0,
                         QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight)  # Place the grid widget next to the other widgets
        layout.addWidget(self.version_label, 0,
                         QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight)

        container = QtWidgets.QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def update_blocks(self):
        self.blocks = block.Block.from_blocks_folder()
        self.blocks_dropdown.clear()
        self.blocks_dropdown.addItems(list(self.blocks.keys()))

    def change_theme(self, theme):
        config = configparser.ConfigParser()
        config.read("config.ini")
        config.set('General', 'theme', theme)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        apply_stylesheet(QtWidgets.QApplication.instance(), theme=theme)

    def load_block(self, block):
        # Logic for loading the block
        print(f"Block loaded: {block}")
        chipmap.clear()
        self.grid_widget.clear()

        chipmap.from_block(self.blocks[block])

        output = chipmap.output()

        for row in range(64):
            for column in range(16):
                if output[row][column] == 2:
                    self.grid_widget.set_square_color(row, column, 'yellow')

        adlink.set_chip_map(1, output)

if __name__ == "__main__":
    # Create a ConfigParser object
    config = configparser.ConfigParser()
    config.read("config.ini")
    theme = config.get('General', 'theme')

    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme=theme)
    main_window = MainWindow()
    main_window.show()

    output_window = OutputWindow()
    output_window.show()

    # Now, redirect standard output to our text widget
    sys.stdout = output_window

    app.exec()