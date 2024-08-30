from PyQt6 import QtWidgets

from view.gridwidget import GridWidget

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