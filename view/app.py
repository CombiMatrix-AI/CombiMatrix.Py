import sys
from PyQt6 import QtWidgets
from qt_material import apply_stylesheet


class SetupWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab_widget = QtWidgets.QTabWidget(self)
        self.tab_widget.addTab(QtWidgets.QWidget(), "Block Definitions")
        self.tab_widget.addTab(QtWidgets.QWidget(), "Block List")
        self.tab_widget.addTab(QtWidgets.QWidget(), "Voltage Definition")
        self.tab_widget.addTab(QtWidgets.QWidget(), "Chip Test")
        self.tab_widget.addTab(QtWidgets.QWidget(), "Machine Setup")
        self.tab_widget.addTab(QtWidgets.QWidget(), "Keithley Setup")
        self.setCentralWidget(self.tab_widget)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window = SetupWindow()
        self.setup_button = QtWidgets.QPushButton("Setup", self)
        self.setup_button.setGeometry(50, 50, 100, 30)
        self.setup_button.clicked.connect(self.setup_window.show)
        self.setCentralWidget(self.setup_button)


def run_app():
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')
    main_window = MainWindow()
    main_window.show()
    app.exec()


if __name__ == "__main__":
    run_app()
