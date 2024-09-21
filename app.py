import configparser
import sys

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QCheckBox, QPushButton
from PyQt6.QtCore import Qt
from qt_material import apply_stylesheet

from mainwindow import MainWindow
from view.debugwindow import DebugWindow


class LaunchWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title and geometry
        self.setWindowTitle("Integrated Self-Driving Laboratory Software Launch")
        self.setGeometry(200, 200, 700, 500)

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create a label for the title
        title = QLabel("Yonder", self)
        title.setProperty('class', 'title')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create checkboxes
        self.robot_checkbox = QCheckBox("Enable Robot Control", self)
        self.par_checkbox = QCheckBox("Enable PAR Control", self)

        # Create a button for launching the program
        launch_button = QPushButton("Launch Program", self)
        launch_button.clicked.connect(self.launch_program)

        # Add widgets to the layout
        layout.addWidget(title)
        layout.addWidget(self.robot_checkbox)
        layout.addWidget(self.par_checkbox)
        layout.addWidget(launch_button)

        # Set the layout for the window
        self.setLayout(layout)

    def launch_program(self):
        debug_window = DebugWindow()
        debug_window.show()
        sys.stdout = debug_window  # Redirect standard output to text widget

        enable_robot = self.robot_checkbox.isChecked()
        enable_par = self.par_checkbox.isChecked()

        main_window = MainWindow(debug_window, enable_robot, enable_par)
        main_window.show()

        self.close()  # Close the launch window


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")

    extra = {
        # Font
        'font_family': 'Courier New',
        'font_size': 14,
    }

    app = QApplication(sys.argv)
    theme = config.get('General', 'theme')
    apply_stylesheet(app, theme=theme, extra=extra, css_file='view/stylesheet.css')

    window = LaunchWindow()
    window.show()

    sys.exit(app.exec())
