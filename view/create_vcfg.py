import os
from PyQt6 import QtWidgets, QtCore

from definitions import ROOT_DIR
from view.gridwidget import GridWidget


class CreateVcfgWindow(QtWidgets.QMainWindow):
    item_created = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Setup Window")
        self.tab_widget = QtWidgets.QTabWidget(self)

        create_cv_config_tab = QtWidgets.QWidget()
        create_cv_config_layout = QtWidgets.QGridLayout(create_cv_config_tab)

        self.create_cv_button = QtWidgets.QPushButton("Create CV Config")
        self.create_cv_button.clicked.connect(self.create_cv)
        create_cv_config_layout.addWidget(self.create_cv_button, 0, 0)

        self.cv_name_input = QtWidgets.QLineEdit(self)
        self.cv_name_input.setPlaceholderText("Enter CV Config Name")
        create_cv_config_layout.addWidget(self.cv_name_input, 0, 1)

        v_start_label = QtWidgets.QLabel("v_start")
        self.v_start_input = QtWidgets.QLineEdit(self)
        self.v_start_input.setText("0.5")

        v_end_label = QtWidgets.QLabel("v_end")
        self.v_end_input = QtWidgets.QLineEdit(self)
        self.v_end_input.setText("1.3")

        v_2_label = QtWidgets.QLabel("v_2")
        self.v_2_input = QtWidgets.QLineEdit(self)
        self.v_2_input.setText("0.2")

        v_final_label = QtWidgets.QLabel("v_final")
        self.v_final_input = QtWidgets.QLineEdit(self)
        self.v_final_input.setText("1.0")

        rate_label = QtWidgets.QLabel("rate")
        self.rate_input = QtWidgets.QLineEdit(self)
        self.rate_input.setText("0.05")

        step_label = QtWidgets.QLabel("step")
        self.step_input = QtWidgets.QLineEdit(self)
        self.step_input.setText("0.001")

        n_cycles_label = QtWidgets.QLabel("n_cycles")
        self.n_cycles_input = QtWidgets.QLineEdit(self)
        self.n_cycles_input.setText("2")

        begin_i_label = QtWidgets.QLabel("begin_i")
        self.begin_i_input = QtWidgets.QLineEdit(self)
        self.begin_i_input.setText("0.5")

        end_i_label = QtWidgets.QLabel("end_i")
        self.end_i_input = QtWidgets.QLineEdit(self)
        self.end_i_input.setText("1.0")

        # Add widgets to the create_cv_config_layout
        create_cv_config_layout.addWidget(v_start_label, 1, 0)
        create_cv_config_layout.addWidget(self.v_start_input, 1, 1)
        create_cv_config_layout.addWidget(v_end_label, 1, 2)
        create_cv_config_layout.addWidget(self.v_end_input, 1, 3)
        create_cv_config_layout.addWidget(v_2_label, 1, 4)
        create_cv_config_layout.addWidget(self.v_2_input, 1, 5)
        create_cv_config_layout.addWidget(v_final_label, 1, 6)
        create_cv_config_layout.addWidget(self.v_final_input, 1, 7)

        create_cv_config_layout.addWidget(rate_label, 2, 0)
        create_cv_config_layout.addWidget(self.rate_input, 2, 1)

        create_cv_config_layout.addWidget(step_label, 3, 0)
        create_cv_config_layout.addWidget(self.step_input, 3, 1)

        create_cv_config_layout.addWidget(n_cycles_label, 4, 0)
        create_cv_config_layout.addWidget(self.n_cycles_input, 4, 1)

        create_cv_config_layout.addWidget(begin_i_label, 5, 0)
        create_cv_config_layout.addWidget(self.begin_i_input, 5, 1)

        create_cv_config_layout.addWidget(end_i_label, 6, 0)
        create_cv_config_layout.addWidget(self.end_i_input, 6, 1)

        ##############################################################################################

        self.tab_widget.addTab(create_cv_config_tab, "Create CV Config")
        self.setCentralWidget(self.tab_widget)

    def create_cv(self):
        start = float(self.v_start_input.text())
        end = float(self.v_end_input.text())
        E2 = float(self.v_2_input.text())
        Ef = float(self.v_final_input.text())
        rate = float(self.rate_input.text())
        step = float(self.step_input.text())
        N_cycles = int(self.n_cycles_input.text())
        begin_measuring_I = float(self.begin_i_input.text())
        End_measuring_I = float(self.end_i_input.text())

        cv_config_content = (
            "[Cyclic Voltammetry Config]\n"
            f"v_start = {start}\n"
            f"v_end = {end}\n"
            f"v_2 = {E2}\n"
            f"v_final = {Ef}\n"
            f"scan rate (V/s) = {rate}\n"
            f"voltage step = {step}\n"
            f"cycles = {N_cycles}\n"
            f"begin_measuring_I = {begin_measuring_I}\n"
            f"End_measuring_I = {End_measuring_I}\n"
        )

        cv_name = self.cv_name_input.text()  # Assuming you want to generate a common name or you can provide input for this

        # Ensure the cv_configs directory exists
        cv_configs_dir = os.path.join(os.path.dirname(__file__), '..', 'vcfgs', 'cv')

        # Write the content to a .cv.vcfg file in the cv_configs folder
        with open(os.path.join(cv_configs_dir, f"{cv_name}.cv.vcfg"), "w") as cv_file:
            cv_file.write(cv_config_content)

        self.item_created.emit(f"CV Config Created, {cv_name}")
