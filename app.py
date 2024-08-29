######################################################################################
# Main UI control of app
######################################################################################

import sys
from PyQt6 import QtWidgets, QtCore
from qt_material import apply_stylesheet
import configparser


# TODO: this clusterfuck of a ui is all in a single file pls fix

class SetupWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab_widget = QtWidgets.QTabWidget(self)
        self.tab_widget.addTab(QtWidgets.QWidget(), "Block Definitions")
        self.tab_widget.addTab(QtWidgets.QWidget(), "Block List")
        self.tab_widget.addTab(QtWidgets.QWidget(), "Voltage Definition")

        # Create the Chip Test tab with a GridWidget
        chip_test_widget = QtWidgets.QWidget()
        chip_test_layout = QtWidgets.QVBoxLayout(chip_test_widget)
        self.grid_widget = GridWidget()
        chip_test_layout.addWidget(self.grid_widget)
        self.tab_widget.addTab(chip_test_widget, "Chip Test")

        self.tab_widget.addTab(QtWidgets.QWidget(), "Machine Setup")
        self.tab_widget.addTab(QtWidgets.QWidget(), "Keithley Setup")
        self.setCentralWidget(self.tab_widget)


class GridWidget(QtWidgets.QWidget):
    def __init__(self, rows=64, columns=16):
        super().__init__()
        self.setFixedSize(columns * 6, rows * 6)  # Set a fixed size for the widget
        self.grid_layout = QtWidgets.QGridLayout(self)
        self.grid_layout.setSpacing(0)  # Set spacing between squares
        self.squares = []

        for row in range(rows):
            row_squares = []
            for col in range(columns):
                square = QtWidgets.QLabel(self)
                square.setFixedSize(6, 6)  # Set a fixed size for the squares
                square.setStyleSheet("background-color: white; border: 1.2px solid black;")
                square.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
                self.grid_layout.addWidget(square, row, col)
                row_squares.append(square)
            self.squares.append(row_squares)

    def set_square_color(self, row, col, color):
        if 0 <= row < len(self.squares) and 0 <= col < len(self.squares[row]):
            self.squares[row][col].setStyleSheet(f"background-color: {color}; border: 1px solid black;")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)  # Bigger is better!!
        self.setup_window = SetupWindow()
        self.setup_button = QtWidgets.QPushButton("Setup", self)
        self.setup_button.setGeometry(50, 50, 100, 30)
        self.setup_button.clicked.connect(self.setup_window.show)

        self.open_button = QtWidgets.QPushButton("Open File", self)
        self.open_button.setGeometry(160, 50, 100, 30)
        self.open_button.clicked.connect(self.open_file_dialog)

        self.grid_widget = GridWidget()

        self.version_label = QtWidgets.QLabel("CombiMatrixAI, App Version: 0.00001", self)
        self.version_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight)

        self.theme_label = QtWidgets.QLabel("Theme:", self)
        self.theme_dropdown = QtWidgets.QComboBox(self)
        self.theme_dropdown.addItems(['dark_amber.xml', 'dark_blue.xml', 'dark_cyan.xml', 'dark_lightgreen.xml',
                                      'dark_pink.xml', 'dark_purple.xml', 'dark_red.xml', 'dark_teal.xml',
                                      'dark_yellow.xml', 'light_amber.xml', 'light_blue.xml', 'light_cyan.xml',
                                      'light_cyan_500.xml', 'light_lightgreen.xml', 'light_pink.xml',
                                      'light_purple.xml', 'light_red.xml', 'light_teal.xml', 'light_yellow.xml'])
        self.theme_dropdown.activated.connect(lambda: self.change_theme(self.theme_dropdown.currentText()))

        self.current_well_label = QtWidgets.QLabel("Current Well:", self)
        self.current_well_textbox = QtWidgets.QLineEdit(self)
        self.current_well_textbox.setReadOnly(True)

        self.output_log_textbox = QtWidgets.QTextEdit(self)
        self.output_log_textbox.setReadOnly(True)
        self.output_log_textbox.setPlaceholderText("Output Log")

        layout = QtWidgets.QHBoxLayout()

        # TODO: pls fix my horrible layout
        layout.addWidget(self.setup_button, 0, QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.open_button, 0, QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.current_well_label, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.current_well_textbox, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.theme_label, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.theme_dropdown, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.grid_widget, 0,
                         QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight)  # Place the grid widget next to the other widgets
        layout.addWidget(self.version_label, 0,
                         QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.output_log_textbox, 1)

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

    def open_file_dialog(self):
        #TODO: AttributeError: type object 'QFileDialog' has no attribute 'Options'
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "",
                                                             "All Files (*);;Python Files (*.py)", options=options)
        if file_name:
            print(f"File chosen: {file_name}")


def run_app():
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read/Access values from the configuration file
    config.read("config.ini")
    theme = config.get('General', 'theme')

    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme=theme)

    main_window = MainWindow()
    main_window.show()
    app.exec()


if __name__ == "__main__":
    run_app()
