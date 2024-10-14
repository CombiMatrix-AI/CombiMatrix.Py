import os
from PyQt6.QtWidgets import QPushButton, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QLabel, \
    QDialog, QLineEdit, QFormLayout, QDialogButtonBox, QMessageBox
from PyQt6 import QtCore
import pandas as pd

from utils.ui_utils import ROOT_DIR, set_counter_electrode, set_working_electrode, set_reference_electrode
from view.experiment_window import ExperimentWindow

# Load the Excel sheet
electrodes_df = pd.read_excel(os.path.join(ROOT_DIR, "database", "Electrodes.xlsx"))
# Filter out rows with any missing values in 'Name' or 'Generally used as:' columns
electrodes_df.dropna(subset=['Name', 'Generally used as:'], inplace=True)
electrodes_db = electrodes_df[['Name', 'Generally used as:']].to_dict(orient='records')

class ChipSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set window title
        self.setWindowTitle("Choose Chip")
        layout = QFormLayout(self)

        # Add wafer design dropdown
        wafer_design_label = QLabel("Wafer Design:", self)
        layout.addWidget(wafer_design_label)
        self.wafer_design = QComboBox(self)
        self.wafer_design.addItems(["CBMX", "NDC-WB", "CMAI-WA"])
        self.wafer_design.setFixedWidth(200)
        self.wafer_design.currentIndexChanged.connect(self.updateLead)
        layout.addWidget(self.wafer_design)

        # Add wafer number dropdown
        wafer_number_label = QLabel("Wafer Number:", self)
        layout.addWidget(wafer_number_label)
        self.wafer_number = QComboBox(self)
        self.wafer_number.addItems([str(i) for i in range(1, 101)])
        self.wafer_number.setFixedWidth(200)
        layout.addWidget(self.wafer_number)

        # Add chip number dropdown
        chip_number_label = QLabel("Chip Number:", self)
        layout.addWidget(chip_number_label)
        self.chip_number = QComboBox(self)
        self.chip_number.addItems([str(i) for i in range(1, 45)])
        self.chip_number.setFixedWidth(200)
        layout.addWidget(self.chip_number)

        # Add lead dropdown
        lead_label = QLabel("Lead (WA and WB only):", self)
        layout.addWidget(lead_label)
        self.lead = QComboBox(self)
        self.lead.addItems([str(i) for i in range(1, 7)])
        self.lead.setFixedWidth(200)
        self.lead.setEnabled(False)
        layout.addWidget(self.lead)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def updateLead(self):
        # Check the value of the first ComboBox
        if self.wafer_design.currentText() == "CMAI-WA" or self.wafer_design.currentText() == "NDC-WB":
            self.lead.setEnabled(True)
        else:
            self.lead.setEnabled(False)

    def accept(self):
        if self.wafer_design.currentText() == "CMAI-WA" or self.wafer_design.currentText() == "NDC-WB":
            self.chip = (f"Chip: {self.wafer_design.currentText()}, {self.wafer_number.currentText()}-{self.chip_number.currentText()},"
                         f" Lead {self.lead.currentText()}")
        else:
            self.chip = f"Chip: {self.wafer_design.currentText()}, {self.wafer_number.currentText()}-{self.chip_number.currentText()}"
        global electrodes_db
        electrodes_db.append({"Name": self.chip, "Generally used as:": "Counter, Working, Reference"})
        super().accept()


class AddElectrodeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add New Electrode")
        layout = QFormLayout(self)
        self.name_input = QLineEdit(self)
        self.generally_used_as_input = QLineEdit(self)

        layout.addRow("Electrode Name:", self.name_input)
        layout.addRow("Generally Used As:", self.generally_used_as_input)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def accept(self):
        name = self.name_input.text().strip()
        generally_used_as = self.generally_used_as_input.text().strip()
        if name and generally_used_as:
            global electrodes_db
            electrodes_db.append({"Name": name, "Generally used as:": generally_used_as})
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
        main_layout.addWidget(title, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)

        h1_layout = QHBoxLayout()
        self.counter_dropdown = QComboBox(self)
        self.counter_dropdown.setFixedWidth(300)
        h1_layout.addWidget(QLabel("Counter:", self))
        h1_layout.addWidget(self.counter_dropdown)

        h2_layout = QHBoxLayout()
        self.reference_dropdown = QComboBox(self)
        self.reference_dropdown.setFixedWidth(300)
        h2_layout.addWidget(QLabel("Reference:", self))
        h2_layout.addWidget(self.reference_dropdown)


        h3_layout = QHBoxLayout()
        self.working_dropdown = QComboBox(self)
        self.working_dropdown.setFixedWidth(300)
        h3_layout.addWidget(QLabel("Working:", self))
        h3_layout.addWidget(self.working_dropdown)

        main_layout.addLayout(h1_layout)
        main_layout.addLayout(h2_layout)
        main_layout.addLayout(h3_layout)

        # Add OK button to start ExperimentWindow
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.start_experiment)
        main_layout.addWidget(self.ok_button, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)

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
        for electrode in electrodes_db:
            generally_used_as_list = [item.strip() for item in electrode["Generally used as:"].split(',')]
            if electrode_type in generally_used_as_list:
                dropdown.addItem(electrode["Name"], electrode)
        if dropdown == self.reference_dropdown:
            dropdown.addItem("Shorted to counter")
        dropdown.addItem("Chip...")
        dropdown.addItem("New...")
        dropdown.currentTextChanged.connect(lambda: self.on_dropdown_change(dropdown))

    def on_dropdown_change(self, dropdown):
        if dropdown.currentText() == "New...":
            dialog = AddElectrodeDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.clear_and_repopulate_dropdowns(dropdown)
                dropdown.setCurrentText(dialog.name_input.text())
            else:
                self.clear_and_repopulate_dropdowns(dropdown)
        elif dropdown.currentText() == "Chip...":
            dialog = ChipSelectionDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.clear_and_repopulate_dropdowns(dropdown)
                dropdown.setCurrentText(dialog.chip)
            else:
                self.clear_and_repopulate_dropdowns(dropdown)

    def clear_and_repopulate_dropdowns(self, dropdown):
        counter_text = self.counter_dropdown.currentText()
        reference_text = self.reference_dropdown.currentText()
        working_text = self.working_dropdown.currentText()

        self.counter_dropdown.clear()
        self.reference_dropdown.clear()
        self.working_dropdown.clear()
        self.populate_all_dropdowns()

        # Restore the old values of the dropdowns where "Chip..." or "New..." wasn't selected
        if dropdown != self.counter_dropdown:
            self.counter_dropdown.setCurrentText(counter_text)
        if dropdown != self.reference_dropdown:
            self.reference_dropdown.setCurrentText(reference_text)
        if dropdown != self.working_dropdown:
            self.working_dropdown.setCurrentText(working_text)

    def start_experiment(self):
        counter_text = self.counter_dropdown.currentText()
        reference_text = self.reference_dropdown.currentText()
        working_text = self.working_dropdown.currentText()

        patterns = ["Chip: NDC-WF", "Chip: CBMX"]
        matches = sum(
            1 for text in [counter_text, reference_text, working_text] if
            any(text.startswith(pattern) for pattern in patterns))
        if matches > 1:
            QMessageBox.warning(self, "Chip Selection Error",
                        "CBMX chip can only be used on one electrode per experiment.")
            return
        else:
            set_counter_electrode(counter_text)
            set_working_electrode(working_text)
            set_reference_electrode(reference_text)

            self.experiment_window = ExperimentWindow()
            self.experiment_window.show()
            self.close()
