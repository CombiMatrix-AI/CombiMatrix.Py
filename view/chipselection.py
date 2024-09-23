from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QCheckBox, QVBoxLayout


class ChipSelectionWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("Chip Selection")

        # Set layout
        layout = QVBoxLayout()

        # Add title label
        title = QLabel("Choose Chip", self)
        layout.addWidget(title)

        # Add wafer design dropdown
        wafer_design_label = QLabel("Wafer Design:", self)
        layout.addWidget(wafer_design_label)
        self.wafer_design = QComboBox(self)
        self.wafer_design.addItems(["CBMX", "NDC-WB", "NDC-WF", "CMAI-WA"])
        layout.addWidget(self.wafer_design)

        # Add wafer number dropdown
        wafer_number_label = QLabel("Wafer Number:", self)
        layout.addWidget(wafer_number_label)
        self.wafer_number = QComboBox(self)
        self.wafer_number.addItems([str(i) for i in range(1, 101)])
        layout.addWidget(self.wafer_number)

        # Add chip number dropdown
        chip_number_label = QLabel("Chip Number:", self)
        layout.addWidget(chip_number_label)
        self.chip_number = QComboBox(self)
        self.chip_number.addItems([str(i) for i in range(1, 45)])
        layout.addWidget(self.chip_number)

        # Add lead checkboxes
        for i in range(1, 7):
            self.lead_checkbox = QCheckBox(f"Lead {i}", self)
            layout.addWidget(self.lead_checkbox)

        # Set the layout for the window
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication([])
    window = ChipSelectionWindow()
    window.show()
    app.exec()
