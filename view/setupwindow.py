from PyQt6 import QtWidgets
import random

from view.gridwidget import GridWidget

class SetupWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Setup Window")
        self.resize(800, 600)

        self.tab_widget = QtWidgets.QTabWidget(self)
        self.tab_widget.addTab(QtWidgets.QWidget(), "Create Block")
        self.setCentralWidget(self.tab_widget)
