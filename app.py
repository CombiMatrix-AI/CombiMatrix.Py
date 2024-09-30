import sys

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QCheckBox, QPushButton, QComboBox, QHBoxLayout, \
    QLineEdit, QGridLayout
from PyQt6.QtCore import Qt
from qt_material import apply_stylesheet

from definitions import CONFIG, SET_ROBOT_ENABLED, SET_PAR_ENABLED
from view.electrodesetup import ElectrodeSetupWindow
from view.debugwindow import DebugWindow

def change_theme(theme):
    CONFIG.set('General', 'theme', theme)
    with open('config.ini', 'w') as configfile:
        CONFIG.write(configfile)
    apply_stylesheet(QApplication.instance(), theme=theme, extra=extra, css_file='view/stylesheet.css')

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
        layout.addWidget(launch_button)

        layout_bottom = QHBoxLayout()
        layout_bottom.addWidget(theme_label, 0, Qt.AlignmentFlag.AlignLeft)
        layout_bottom.addWidget(theme_dropdown, 10, Qt.AlignmentFlag.AlignLeft)
        layout_bottom.addWidget(QLabel("Yonder, App Version: Pre-Beta"), 0, Qt.AlignmentFlag.AlignRight)
        layout.addLayout(layout_bottom)

        self.setLayout(layout)

    def launch_program(self):
        CONFIG.set('General', 'user', self.user_input.text())
        CONFIG.set('General', 'customer', self.customer_input.text())
        with open('config.ini', 'w') as configfile:
            CONFIG.write(configfile)

        debug_window = DebugWindow()
        debug_window.show()
        sys.stdout = debug_window  # Redirect standard output to text widget

        SET_ROBOT_ENABLED(self.robot_checkbox.isChecked())
        SET_PAR_ENABLED(self.par_checkbox.isChecked())

        electrode_setup = ElectrodeSetupWindow()
        electrode_setup.show()

        self.close()  # Close the launch window


if __name__ == "__main__":
    extra = {
        # Font
        'font_family': 'Courier New',
        'font_size': 14,
    }

    app = QApplication(sys.argv)
    theme = CONFIG.get('General', 'theme')
    apply_stylesheet(app, theme=theme, extra=extra, css_file='view/stylesheet.css')

    window = LaunchWindow()
    window.show()

    sys.exit(app.exec())
