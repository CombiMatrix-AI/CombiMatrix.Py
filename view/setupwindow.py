import os
from PyQt6 import QtWidgets, QtCore

from view.gridwidget import GridWidget


class SetupWindow(QtWidgets.QMainWindow):
    item_created = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Setup Window")
        self.tab_widget = QtWidgets.QTabWidget(self)

        ##############################################################################################

        create_block_tab = QtWidgets.QWidget()
        create_block_layout = QtWidgets.QHBoxLayout(create_block_tab)

        create_block_button_sublayout = QtWidgets.QVBoxLayout()
        self.block_name_input = QtWidgets.QLineEdit(self)
        self.block_name_input.setPlaceholderText("Enter Block Name")
        create_block_button_sublayout.addWidget(self.block_name_input, 0,
                                                QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.create_block_button = QtWidgets.QPushButton("Create Block")
        self.create_block_button.clicked.connect(self.create_block)
        create_block_button_sublayout.addWidget(self.create_block_button, 0,
                                                QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.clear_grid_button = QtWidgets.QPushButton("Clear Grid")
        self.clear_grid_button.clicked.connect(lambda: self.grid_widget.clear())
        create_block_button_sublayout.addWidget(self.clear_grid_button, 0,
                                                QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        spacer = QtWidgets.QSpacerItem(200, 300, QtWidgets.QSizePolicy.Policy.Fixed,
                                       QtWidgets.QSizePolicy.Policy.Minimum)
        create_block_button_sublayout.addItem(spacer)

        create_block_layout.addLayout(create_block_button_sublayout, 0)

        self.block_chipmap = [[0] * 16 for _ in range(64)]
        self.grid_widget = GridWidget(8, self.block_chipmap)
        create_block_layout.addWidget(self.grid_widget, 0,
                                      QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight)

        ##############################################################################################

        create_cv_config_tab = QtWidgets.QWidget()
        create_cv_config_layout = QtWidgets.QGridLayout(create_cv_config_tab)

        self.create_cv_button = QtWidgets.QPushButton("Create CV Config")
        self.create_cv_button.clicked.connect(self.create_cv)
        create_cv_config_layout.addWidget(self.create_cv_button, 0, 0)

        self.cv_name_input = QtWidgets.QLineEdit(self)
        self.cv_name_input.setPlaceholderText("Enter CV Config Name")
        create_cv_config_layout.addWidget(self.cv_name_input, 0, 1)

        # Create labels and input fields for vs_init, v_step, scan_rate, etc.
        vs_init_label = QtWidgets.QLabel("vs_init")
        self.vs_init_input = [QtWidgets.QCheckBox(f"Scan {i + 1}") for i in range(5)]

        v_step_label = QtWidgets.QLabel("v_step")
        self.v_step_input = [QtWidgets.QLineEdit(self) for _ in range(5)]
        for idx, value in enumerate([0.6, 1.9, 0, 0.6, 0.6]):
            self.v_step_input[idx].setText(str(value))

        scan_rate_label = QtWidgets.QLabel("scan_rate")
        self.scan_rate_input = [QtWidgets.QLineEdit(self) for _ in range(5)]
        for idx, value in enumerate([800.0, 800.0, 800.0, 800.0, 800.0]):
            self.scan_rate_input[idx].setText(str(value))

        record_de_label = QtWidgets.QLabel("record_de")
        self.record_de_input = QtWidgets.QLineEdit(self)
        self.record_de_input.setText("0.01")

        average_de_label = QtWidgets.QLabel("average_de")
        self.average_de_input = QtWidgets.QCheckBox()
        self.average_de_input.setChecked(True)

        n_cycles_label = QtWidgets.QLabel("n_cycles")
        self.n_cycles_input = QtWidgets.QLineEdit(self)
        self.n_cycles_input.setText("25")

        begin_i_label = QtWidgets.QLabel("begin_i")
        self.begin_i_input = QtWidgets.QLineEdit(self)
        self.begin_i_input.setText("0.98")

        end_i_label = QtWidgets.QLabel("end_i")
        self.end_i_input = QtWidgets.QLineEdit(self)
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

        self.tab_widget.addTab(create_block_tab, "Create Block")
        self.tab_widget.addTab(create_cv_config_tab, "Create CV Config")
        self.setCentralWidget(self.tab_widget)

    def create_block(self):  # TODO: MOVE LOGIC TO BLOCKS FOLDER?
        first_row, first_col = -1, -1
        last_row, last_col = -1, -1

        for row in range(len(self.block_chipmap)):
            for col in range(len(self.block_chipmap[0])):
                if self.block_chipmap[row][col] != 0:
                    if first_row == -1 or row < first_row:
                        first_row = row
                    if first_col == -1 or col < first_col:
                        first_col = col
                    if row > last_row:
                        last_row = row
                    if col > last_col:
                        last_col = col

        width = last_row - first_row + 1 if first_row != -1 else 0
        length = last_col - first_col + 1 if first_col != -1 else 0

        block_definition = ""
        for row in range(first_row, last_row + 1):
            for col in range(first_col, last_col + 1):
                block_definition += str(self.block_chipmap[row][col])

        block_name = self.block_name_input.text()

        # Create the content for the .block file
        block_file_content = (
            "[Block]\n"
            f"Number rows = {width}\n"
            f"Number columns = {length}\n"
            f"Start row = {first_row}\n"
            f"Start column = {first_col}\n"
            f'Definition = "{block_definition}"\n'
        )

        # Ensure the blocks directory exists
        blocks_dir = os.path.join(os.path.dirname(__file__), '..', 'blocks')

        # Write the content to a .block file in the blocks folder
        with open(os.path.join(blocks_dir, f"{block_name}.block"), "w") as block_file:
            block_file.write(block_file_content)

        self.grid_widget.clear()
        self.item_created.emit(f"Block Created, {block_name}")

    def create_cv(self):
        vs_init_vals = [chk.isChecked() for chk in self.vs_init_input]
        v_step_vals = [float(ledit.text()) for ledit in self.v_step_input]
        scan_rate_vals = [float(ledit.text()) for ledit in self.scan_rate_input]
        record_de_val = float(self.record_de_input.text())
        average_de_val = self.average_de_input.isChecked()
        n_cycles_val = int(self.n_cycles_input.text())
        begin_i_val = float(self.begin_i_input.text())
        end_i_val = float(self.end_i_input.text())

        cv_config_content = (
            "[Cyclic Voltammetry Config]\n"
            f"vs_init = {vs_init_vals}\n"
            f"v_step = {v_step_vals}\n"
            f"scan_rate = {scan_rate_vals}\n"
            f"record_de = {record_de_val}\n"
            f"average_de = {average_de_val}\n"
            f"n_cycles = {n_cycles_val}\n"
            f"begin_i = {begin_i_val}\n"
            f"end_i = {end_i_val}\n"
        )

        cv_name = self.cv_name_input.text()  # Assuming you want to generate a common name or you can provide input for this

        # Ensure the cv_configs directory exists
        cv_configs_dir = os.path.join(os.path.dirname(__file__), '..', 'vcfgs', 'cv')

        # Write the content to a .cv.vcfg file in the cv_configs folder
        with open(os.path.join(cv_configs_dir, f"{cv_name}.cv.vcfg"), "w") as cv_file:
            cv_file.write(cv_config_content)

        self.item_created.emit(f"CV Config Created, {cv_name}")
