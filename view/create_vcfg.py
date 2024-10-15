import json

from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QGridLayout, QPushButton, QLineEdit, QLabel, QCheckBox
from PyQt6.QtCore import pyqtSignal

from utils.ui_utils import ROOT_DIR


class CreateVcfgWindow(QMainWindow):
    item_created = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Setup Window")
        self.tab_widget = QTabWidget(self)

        ##############################################################################################

        create_cv_config_tab = QWidget()
        create_cv_config_layout = QGridLayout(create_cv_config_tab)

        self.create_cv_button = QPushButton("Create CV Config")
        self.create_cv_button.clicked.connect(self.create_cv)
        create_cv_config_layout.addWidget(self.create_cv_button, 0, 0)

        self.cv_name_input = QLineEdit(self)
        self.cv_name_input.setPlaceholderText("Enter CV Config Name")
        create_cv_config_layout.addWidget(self.cv_name_input, 0, 1)

        # Create labels and input fields for vs_init, v_step, scan_rate, etc.
        vs_init_label = QLabel("vs_init")
        self.vs_init_input = [QCheckBox(f"Scan {i + 1}") for i in range(5)]

        v_step_label = QLabel("v_step")
        self.v_step_input = [QLineEdit(self) for _ in range(5)]
        for idx, value in enumerate([0.6, 1.9, 0, 0.6, 0.6]):
            self.v_step_input[idx].setText(str(value))

        scan_rate_label = QLabel("scan_rate")
        self.scan_rate_input = [QLineEdit(self) for _ in range(5)]
        for idx, value in enumerate([800.0, 800.0, 800.0, 800.0, 800.0]):
            self.scan_rate_input[idx].setText(str(value))

        record_de_label = QLabel("record_de")
        self.record_de_input = QLineEdit(self)
        self.record_de_input.setText("0.01")

        average_de_label = QLabel("average_de")
        self.average_de_input = QCheckBox()
        self.average_de_input.setChecked(True)

        n_cycles_label = QLabel("n_cycles")
        self.n_cycles_input = QLineEdit(self)
        self.n_cycles_input.setText("25")

        begin_i_label = QLabel("begin_i")
        self.begin_i_input = QLineEdit(self)
        self.begin_i_input.setText("0.98")

        end_i_label = QLabel("end_i")
        self.end_i_input = QLineEdit(self)
        self.end_i_input.setText("1")

        # Add widgets to the create_cv_config_layout
        create_cv_config_layout.addWidget(vs_init_label, 1, 0)
        for i, checkbox in enumerate(self.vs_init_input, start=1):
            create_cv_config_layout.addWidget(checkbox, 1, i)

        create_cv_config_layout.addWidget(v_step_label, 2, 0)
        for i, line_edit in enumerate(self.v_step_input, start=1):
            create_cv_config_layout.addWidget(line_edit, 2, i)

        create_cv_config_layout.addWidget(scan_rate_label, 3, 0)
        for i, line_edit in enumerate(self.scan_rate_input, start=1):
            create_cv_config_layout.addWidget(line_edit, 3, i)

        create_cv_config_layout.addWidget(record_de_label, 4, 0)
        create_cv_config_layout.addWidget(self.record_de_input, 4, 1)

        create_cv_config_layout.addWidget(average_de_label, 5, 0)
        create_cv_config_layout.addWidget(self.average_de_input, 5, 1)

        create_cv_config_layout.addWidget(n_cycles_label, 6, 0)
        create_cv_config_layout.addWidget(self.n_cycles_input, 6, 1)

        create_cv_config_layout.addWidget(begin_i_label, 7, 0)
        create_cv_config_layout.addWidget(self.begin_i_input, 7, 1)

        create_cv_config_layout.addWidget(end_i_label, 8, 0)
        create_cv_config_layout.addWidget(self.end_i_input, 8, 1)

        ##############################################################################################

        self.tab_widget.addTab(create_cv_config_tab, "Create CV Config")
        self.setCentralWidget(self.tab_widget)

    def create_cv(self):
        vs_init_vals = [chk.isChecked() for chk in self.vs_init_input]
        v_step_vals = [float(ledit.text()) for ledit in self.v_step_input]
        scan_rate_vals = [float(ledit.text()) for ledit in self.scan_rate_input]
        record_de_val = float(self.record_de_input.text())
        average_de_val = self.average_de_input.isChecked()
        n_cycles_val = int(self.n_cycles_input.text())
        begin_i_val = float(self.begin_i_input.text())
        end_i_val = float(self.end_i_input.text())

        cv_config_dict = {
            "vs_initial": vs_init_vals,
            "Voltage_step": v_step_vals,
            "Scan_Rate": scan_rate_vals,
            "Scan_number": 2,
            "Record_every_dE": record_de_val,
            "Average_over_dE": average_de_val,
            "N_Cycles": n_cycles_val,
            "Begin_measuring_I": begin_i_val,
            "End_measuring_I": end_i_val
        }

        cv_name = f"{self.cv_name_input.text()}.cv"  # Assuming you want to generate a common name or you can provide input for this

        # Write the content to a .cv.vcfg file in the cv_configs folder
        with open(ROOT_DIR / 'vcfgs' / f"{cv_name}.vcfg", "w") as cv_file:
            json.dump(cv_config_dict, cv_file, indent=4)

        self.item_created.emit(f"PAR Config Created, {cv_name}")
