import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QLabel, \
    QPushButton, QDialog, QLineEdit, QFormLayout, QDialogButtonBox, QMessageBox
from PyQt6.QtCore import Qt

# Simulated electrodes database
electrodes_db = [
    {"name": "Electrode A", "generally_used_as": "Counter"},
    {"name": "Electrode B", "generally_used_as": "Reference"},
    {"name": "Electrode C", "generally_used_as": "Counter, Working"},
]


class AddElectrodeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add New Electrode")
        self.layout = QFormLayout(self)
        self.name_input = QLineEdit(self)
        self.generally_used_as_input = QLineEdit(self)

        self.layout.addRow("Electrode Name:", self.name_input)
        self.layout.addRow("Generally Used As:", self.generally_used_as_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
                                        self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.buttons)

    def accept(self):
        name = self.name_input.text().strip()
        generally_used_as = self.generally_used_as_input.text().strip()
        if name and generally_used_as:
            global electrodes_db
            electrodes_db.append({"name": name, "generally_used_as": generally_used_as})
            super().accept()
        else:
            QMessageBox.warning(self, "Input Error", "Please provide both name and 'generally used as' fields.")


class ElectrodeSetupWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Electrode Setup")

        title = QLabel("Electrode Setup", self)
        title.setProperty('class', 'title')

        main_layout = QVBoxLayout()

        main_layout.addWidget(title, 0, Qt.AlignmentFlag.AlignHCenter)

        h_layout = QHBoxLayout()

        self.counter_dropdown = QComboBox()
        h_layout.addWidget(QLabel("Counter:"))
        h_layout.addWidget(self.counter_dropdown)

        self.reference_dropdown = QComboBox()
        h_layout.addWidget(QLabel("Reference Electrode:"))
        h_layout.addWidget(self.reference_dropdown)

        self.working_dropdown = QComboBox()
        h_layout.addWidget(QLabel("Working Electrode:"))
        h_layout.addWidget(self.working_dropdown)

        main_layout.addLayout(h_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Populate dropdowns after the UI elements are created
        self.populate_all_dropdowns()

    def populate_all_dropdowns(self):
        self.populate_dropdown(self.counter_dropdown, "Counter")
        self.populate_dropdown(self.reference_dropdown, "Reference")
        self.populate_dropdown(self.working_dropdown, "Working")

    def populate_dropdown(self, dropdown, electrode_type):
        sorted_electrodes = sorted(electrodes_db, key=lambda x: x['generally_used_as'])
        for electrode in sorted_electrodes:
            generally_used_as_list = [item.strip() for item in electrode["generally_used_as"].split(',')]
            if electrode_type in generally_used_as_list:
                dropdown.addItem(electrode["name"], electrode)
        dropdown.addItem("Chip...")
        dropdown.addItem("New...")
        dropdown.currentTextChanged.connect(lambda: self.on_dropdown_change(dropdown, electrode_type))

    def on_dropdown_change(self, dropdown, electrode_type):
        if dropdown.currentText() == "New...":
            dialog = AddElectrodeDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.clear_and_repopulate_dropdowns()
                dropdown.setCurrentText(dialog.name_input.text())
        elif dropdown.currentText() == "Chip...":
            QMessageBox.information(self, "Select Chip", f"Open {electrode_type} chip selection screen.")

    def clear_and_repopulate_dropdowns(self):
        self.counter_dropdown.clear()
        self.reference_dropdown.clear()
        self.working_dropdown.clear()
        self.populate_all_dropdowns()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_win = ElectrodeSetupWindow()
    main_win.show()

    sys.exit(app.exec())
