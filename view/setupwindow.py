from PyQt6 import QtWidgets
import random

from view.gridwidget import GridWidget
from app import adlink


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

        # Adding a button to run chip test
        self.chip_test_button = QtWidgets.QPushButton("Chip Test")
        self.chip_test_button.clicked.connect(lambda: self.chip_test(1))  # Assuming channel 1 for testing
        chip_test_layout.addWidget(self.chip_test_button)

        self.tab_widget.addTab(chip_test_widget, "Chip Test")

        self.tab_widget.addTab(QtWidgets.QWidget(), "Machine Setup")
        self.tab_widget.addTab(QtWidgets.QWidget(), "Keithley Setup")
        self.setCentralWidget(self.tab_widget)

    def chip_test(self, channel):
        for i in range(7):
            if i == 1:
                chipmap_in = [0] * 1024
            elif i == 2:
                chipmap_in = [1] * 1024
            elif i == 3:
                chipmap_in = [2] * 1024
            elif i == 4:
                chipmap_in = [3] * 1024
            elif i == 5:
                chipmap_in = [1 if j % 2 == 0 else 2 for j in range(1024)]
            elif i == 6:
                chipmap_in = [2 if k % 2 == 0 else 3 for k in range(1024)]
            elif i == 7:
                chipmap_in = [random.randint(0, 3) for _ in range(1024)]

            chipmap_out = [0] * 1024

            adlink.set_chip_map(channel, chipmap_in)
            adlink.get_chip_map(channel, chipmap_out)

            if chipmap_in == chipmap_out:
                self.output_log_textbox.append(f"Test {i} Passed")
            else:
                self.output_log_textbox.append(f"Test {i} Failed")
                differences = [(l, chipmap_in[l], chipmap_out[l]) for l in range(len(chipmap_in)) if
                               chipmap_in[l] != chipmap_out[l]]
                # Print differences
                for index, value1, value2 in differences:
                    print(f"Index {index}: list1 has {value1}, list2 has {value2}")
