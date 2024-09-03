import configparser
from PyQt6 import QtWidgets, QtCore
from qt_material import apply_stylesheet

from view.gridwidget import GridWidget
from view.setupwindow import SetupWindow
#from init import *

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CombiMatrixAI")
        self.resize(800, 600)  # Bigger is better!!
        self.setup_window = SetupWindow()

        self.setup_button = QtWidgets.QPushButton("Setup", self)
        self.setup_button.setGeometry(50, 50, 100, 30)
        self.setup_button.clicked.connect(self.setup_window.show)

        self.open_button = QtWidgets.QPushButton("Open File", self)
        self.open_button.setGeometry(160, 50, 100, 30)
        self.open_button.clicked.connect(self.open_file_dialog)

        self.start_button = QtWidgets.QPushButton("Start", self)  # New start button
        self.start_button.setGeometry(380, 50, 100, 30)  # Positioning the button
        self.start_button.clicked.connect(self.start)

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

        self.current_well_label = QtWidgets.QLabel("Current Well:", self)
        self.current_well_textbox = QtWidgets.QLineEdit(self)
        self.current_well_textbox.setReadOnly(True)

        layout = QtWidgets.QHBoxLayout()

        # TODO: pls fix my horrible layout
        layout.addWidget(self.setup_button, 0, QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.open_button, 0, QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.start_button, 0,
                         QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)  # Adding the start button to the layout
        layout.addWidget(self.current_well_label, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.current_well_textbox, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.theme_label, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.theme_dropdown, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
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

    def open_file_dialog(self):
        # TODO: AttributeError: type object 'QFileDialog' has no attribute 'Options'
        print("test")
        # options = QtWidgets.QFileDialog.options()
        # file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "",
        #                                                     "All Files (*);;Python Files (*.py)", options=options)
        # if file_name:
        #    print(f"File chosen: {file_name}")

    def start(self):
        # Add the main function logic here
        print("Main function started")
        chipmap = [0] * (984 - 160) + [2] * 40 + [0] * 160

        adlink.set_chip_map(1, chipmap)


