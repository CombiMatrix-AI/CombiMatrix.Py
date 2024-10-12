import platform
import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QCheckBox, QPushButton, QComboBox, QHBoxLayout, \
    QLineEdit, QGridLayout, QMessageBox
from PyQt6.QtCore import Qt
from qt_material import apply_stylesheet

from definitions import CONFIG, SET_ROBOT_ENABLED, SET_PAR_ENABLED
from view.combi_control import CombiControlWindow
from view.electrode_setup import ElectrodeSetupWindow
from view.debug_window import DebugWindow

def change_theme(theme):
    CONFIG.set('General', 'theme', theme)
    with open(Path(__file__).parent /'config.ini', 'w') as configfile:
        CONFIG.write(configfile)
    apply_stylesheet(QApplication.instance(), theme=theme, extra=extra, css_file='view/stylesheet.css')


import json
from db_utils import get_connection, is_valid_connection


class LaunchWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title and geometry
        self.setWindowTitle("Integrated Self-Driving Laboratory Software Launch")
        self.setGeometry(100, 100, 600, 400)

        # Create a label for the title
        title = QLabel("Yonder Lab Control", self)
        title.setProperty('class', 'title')

        self.user_input = QLineEdit(self)
        self.user_input.setText(CONFIG.get('General', 'user'))
        self.customer_input = QLineEdit(self)
        self.customer_input.setText(CONFIG.get('General', 'customer'))

        # Create checkboxes
        self.robot_checkbox = QCheckBox("Enable Robot Control", self)
        self.par_checkbox = QCheckBox("Enable PAR Control", self)

        # Create a button for launching the program
        launch_button = QPushButton("Launch Program", self)
        launch_button.clicked.connect(self.launch_program)
        combi_button = QPushButton("Program Combi Chip Only", self)
        combi_button.clicked.connect(self.launch_combi)

        theme_label = QLabel("Theme:", self)
        theme_dropdown = QComboBox(self)
        theme_dropdown.addItems(
            ['dark_amber.xml', 'dark_blue.xml', 'dark_cyan.xml', 'dark_lightgreen.xml', 'dark_pink.xml',
             'dark_purple.xml', 'dark_red.xml', 'dark_teal.xml', 'dark_yellow.xml', 'light_amber.xml', 'light_blue.xml',
             'light_cyan.xml', 'light_cyan_500.xml', 'light_lightgreen.xml', 'light_pink.xml', 'light_purple.xml',
             'light_red.xml', 'light_teal.xml', 'light_yellow.xml'])
        theme_dropdown.setCurrentText(theme)
        theme_dropdown.activated.connect(lambda: change_theme(theme_dropdown.currentText()))

        # Create a vertical layout
        layout = QVBoxLayout()

        layout_top = QGridLayout()
        layout_top.addWidget(QLabel("User:", self), 0, 0)
        layout_top.addWidget(self.user_input, 0, 1)
        layout_top.addWidget(QLabel("Customer:", self), 0, 2)
        layout_top.addWidget(self.customer_input, 0, 3)
        layout.addLayout(layout_top)

        layout.addWidget(title, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.robot_checkbox)
        layout.addWidget(self.par_checkbox)

        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(launch_button)
        layout_buttons.addWidget(combi_button)
        layout.addLayout(layout_buttons)

        layout_bottom = QHBoxLayout()
        layout_bottom.addWidget(theme_label, 0, Qt.AlignmentFlag.AlignLeft)
        layout_bottom.addWidget(theme_dropdown, 10, Qt.AlignmentFlag.AlignLeft)
        layout_bottom.addWidget(QLabel("Yonder, App Version: Pre-Beta"), 0, Qt.AlignmentFlag.AlignRight)
        layout.addLayout(layout_bottom)

        self.setLayout(layout)

    def launch_program(self):
        CONFIG.set('General', 'user', self.user_input.text())
        CONFIG.set('General', 'customer', self.customer_input.text())
        with open(Path(__file__).parent / 'config.ini', 'w') as configfile:
            CONFIG.write(configfile)

        # Get database connection credentials
        creds_path = CONFIG.get('Keys', 'path_to_db_creds')
        try:
            with open(creds_path, 'r') as file:
                credentials = json.load(file)
        except FileNotFoundError:
            QMessageBox.warning(self, "File Not Found",
                                "The database credentials file was not found. Please check the path and try again.")
            return

        # Check if the database connection is valid
        con = get_connection(credentials)
        if platform.system() != 'Darwin': # Don't check on Loren's computer
            if not is_valid_connection(con):
                QMessageBox.warning(self, "No Database Connection",
                            "Invalid database connection. Please check your credentials.")
                return

        self.debug_window = DebugWindow()
        self.debug_window.show()
        sys.stdout = self.debug_window  # Redirect standard output to text widget

        print("Connected to database")

        SET_ROBOT_ENABLED(self.robot_checkbox.isChecked())
        SET_PAR_ENABLED(self.par_checkbox.isChecked())

        self.electrode_setup = ElectrodeSetupWindow()
        self.electrode_setup.show()

        self.close()  # Close the launch window

    def launch_combi(self):
        self.debug_window = DebugWindow()
        self.debug_window.show()
        sys.stdout = self.debug_window  # Redirect standard output to text widget

        self.combi_window = CombiControlWindow()
        self.combi_window.show()

        self.close()  # Close the launch window


if __name__ == "__main__":
    extra = {
        # Font
        'font_family': 'Courier New',
    }

    app = QApplication(sys.argv)
    theme = CONFIG.get('General', 'theme')
    apply_stylesheet(app, theme=theme, extra=extra, css_file='view/stylesheet.css')

    window = LaunchWindow()
    window.show()

    sys.exit(app.exec())
